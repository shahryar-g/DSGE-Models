from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from openpyxl import Workbook

from dsge.core.simulation import simulate_linear_model
from dsge.models.registry import available_models
from dsge.solvers.registry import available_solvers


def _load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _print_matrix(name: str, matrix: np.ndarray, precision: int = 4) -> None:
    print(f"{name} =")
    print(np.array2string(matrix, precision=precision, suppress_small=True))


def _create_run_dir(output_root: Path, model_name: str) -> Path:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / model_name / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _compute_irf(F: np.ndarray, G: np.ndarray, horizon: int, shock_idx: int, size: float) -> np.ndarray:
    n_states = F.shape[0]
    irf = np.zeros((horizon + 1, n_states), dtype=float)
    shock_impact = np.zeros(G.shape[1], dtype=float)
    shock_impact[shock_idx] = size

    irf[1] = G @ shock_impact
    for h in range(1, horizon):
        irf[h + 1] = F @ irf[h]
    return irf


def _style_plot() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")


def _save_irf_matrix_plot(
    solver_dir: Path,
    state_names: list[str],
    shock_names: list[str],
    F: np.ndarray,
    G: np.ndarray,
    irf_horizon: int,
    shock_size: float,
) -> None:
    _style_plot()
    irf_dir = solver_dir / "irf"
    irf_dir.mkdir(parents=True, exist_ok=True)

    t = np.arange(irf_horizon + 1)
    n_states = len(state_names)
    n_shocks = len(shock_names)

    fig, axes = plt.subplots(
        n_states,
        n_shocks,
        figsize=(4.3 * n_shocks, 2.9 * n_states),
        squeeze=False,
    )

    palette = ["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd"]
    for i, state in enumerate(state_names):
        for j, shock in enumerate(shock_names):
            irf = _compute_irf(F=F, G=G, horizon=irf_horizon, shock_idx=j, size=shock_size)
            ax = axes[i, j]
            ax.plot(t, irf[:, i], color=palette[i % len(palette)], linewidth=2.1)
            ax.fill_between(t, 0.0, irf[:, i], alpha=0.15, color=palette[i % len(palette)])
            ax.axhline(0.0, color="#2f2f2f", linewidth=0.9)
            ax.set_facecolor("#fafafa")
            ax.grid(alpha=0.25, linestyle="--", linewidth=0.6)
            if i == 0:
                ax.set_title(shock, fontsize=11, fontweight="semibold")
            if j == 0:
                ax.set_ylabel(state, fontsize=10)
            if i == n_states - 1:
                ax.set_xlabel("horizon", fontsize=10)

    fig.suptitle("Impulse Response Matrix (variables x shocks)", fontsize=14, fontweight="bold", y=0.995)
    fig.tight_layout()
    fig.savefig(irf_dir / "irf_matrix.png", dpi=220)
    plt.close(fig)


def _save_steady_state_plot(
    solver_dir: Path,
    state_names: list[str],
    trajectory: np.ndarray,
    steady_state: np.ndarray,
) -> None:
    _style_plot()
    steady_dir = solver_dir / "steady_state"
    steady_dir.mkdir(parents=True, exist_ok=True)

    t = np.arange(trajectory.shape[0])
    fig, axes = plt.subplots(len(state_names), 1, figsize=(10, 2.8 * len(state_names)), squeeze=False)
    palette = ["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd"]

    for i, state in enumerate(state_names):
        ax = axes[i, 0]
        color = palette[i % len(palette)]
        ax.plot(t, trajectory[:, i], color=color, linewidth=2.0, label="state path")
        ax.axhline(float(steady_state[i]), color="#111111", linestyle="--", linewidth=1.2, label="steady state")
        ax.fill_between(t, steady_state[i], trajectory[:, i], color=color, alpha=0.12)
        ax.set_ylabel(state, fontsize=10)
        ax.set_facecolor("#fafafa")
        ax.grid(alpha=0.25, linestyle="--", linewidth=0.6)

    axes[-1, 0].set_xlabel("time", fontsize=10)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", frameon=True)
    fig.suptitle("States vs Steady State", fontsize=14, fontweight="bold", y=0.995)
    fig.tight_layout()
    fig.savefig(steady_dir / "states_vs_steady.png", dpi=220)
    plt.close(fig)


def _resolve_steady_state(cfg: dict, state_names: list[str]) -> np.ndarray:
    cfg_ss = cfg.get("steady_state")
    if cfg_ss is None:
        return np.zeros(len(state_names), dtype=float)
    return np.array([float(cfg_ss.get(name, 0.0)) for name in state_names], dtype=float)


def _build_excel(run_dir: Path, state_names: list[str], series_by_solver: dict[str, np.ndarray]) -> None:
    wb = Workbook()
    wb.remove(wb.active)

    for solver_name, trajectory in series_by_solver.items():
        ws = wb.create_sheet(title=solver_name[:31])
        ws.append(["t", *state_names])
        for t, row in enumerate(trajectory):
            ws.append([t, *[float(v) for v in row]])

    wb.save(run_dir / "timeseries.xlsx")


def run(config_path: Path, output_root: Path) -> None:
    cfg = _load_config(config_path)
    model_name = cfg["model"]

    model_map = available_models()
    if model_name not in model_map:
        supported = ", ".join(sorted(model_map.keys()))
        raise ValueError(f"Unsupported model: {model_name}. Available models: {supported}")

    run_dir = _create_run_dir(output_root=output_root, model_name=model_name)
    print(f"Results directory: {run_dir}")

    model = model_map[model_name]
    params = cfg["params"]
    horizon = int(cfg.get("horizon", 40))
    seed = int(cfg.get("seed", 0))
    irf_horizon = int(cfg.get("irf_horizon", horizon))
    irf_shock_size = float(cfg.get("irf_shock_size", 1.0))
    steady_state = _resolve_steady_state(cfg=cfg, state_names=model.state_names)

    solver_map = available_solvers()
    requested = cfg.get("solvers", list(solver_map.keys()))
    series_by_solver: dict[str, np.ndarray] = {}

    for solver_name in requested:
        solver = solver_map[solver_name]
        sol = solver.solve(model, params)
        x, _ = simulate_linear_model(sol.F, sol.G, horizon=horizon, seed=seed)
        series_by_solver[solver_name] = x

        solver_dir = run_dir / solver_name
        solver_dir.mkdir(parents=True, exist_ok=True)
        _save_irf_matrix_plot(
            solver_dir=solver_dir,
            state_names=model.state_names,
            shock_names=model.shock_names,
            F=sol.F,
            G=sol.G,
            irf_horizon=irf_horizon,
            shock_size=irf_shock_size,
        )
        _save_steady_state_plot(
            solver_dir=solver_dir,
            state_names=model.state_names,
            trajectory=x,
            steady_state=steady_state,
        )

        print("=" * 72)
        print(f"solver: {solver_name}")
        print(f"stable: {sol.stable} | spectral radius: {sol.spectral_radius:.4f}")
        _print_matrix("F", sol.F)
        _print_matrix("G", sol.G)

    _build_excel(run_dir=run_dir, state_names=model.state_names, series_by_solver=series_by_solver)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DSGE model across solvers")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("src/dsge/configs/nk_model.yaml"),
        help="Path to YAML config",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("result"),
        help="Root directory for saved results",
    )
    args = parser.parse_args()
    run(config_path=args.config, output_root=args.output)


if __name__ == "__main__":
    main()
