from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

from dsge.core.simulation import simulate_linear_model
from dsge.models.toy_nk import ToyNKModel
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


def _write_trajectory_csv(path: Path, state_names: list[str], trajectory: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["t", *state_names])
        for t, row in enumerate(trajectory):
            writer.writerow([t, *row.tolist()])


def _save_state_plot(path: Path, state_names: list[str], trajectory: np.ndarray, solver_name: str) -> None:
    t = np.arange(trajectory.shape[0])
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, state in enumerate(state_names):
        ax.plot(t, trajectory[:, i], label=state)
    ax.set_title(f"State Trajectories - {solver_name}")
    ax.set_xlabel("t")
    ax.set_ylabel("value")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_solver_outputs(
    run_dir: Path,
    solver_name: str,
    state_names: list[str],
    sol_F: np.ndarray,
    sol_G: np.ndarray,
    stable: bool,
    spectral_radius: float,
    trajectory: np.ndarray,
) -> None:
    solver_dir = run_dir / solver_name
    solver_dir.mkdir(parents=True, exist_ok=True)

    np.savetxt(solver_dir / "F.csv", sol_F, delimiter=",")
    np.savetxt(solver_dir / "G.csv", sol_G, delimiter=",")
    _write_trajectory_csv(solver_dir / "trajectory.csv", state_names, trajectory)
    _save_state_plot(solver_dir / "states.png", state_names, trajectory, solver_name)

    summary = {
        "solver": solver_name,
        "stable": stable,
        "spectral_radius": float(spectral_radius),
        "final_state": {
            k: float(v) for k, v in zip(state_names, trajectory[-1], strict=False)
        },
    }
    with (solver_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def run(config_path: Path, output_root: Path) -> None:
    cfg = _load_config(config_path)
    model_name = cfg["model"]
    if model_name != "toy_nk":
        raise ValueError(f"Unsupported model in this starter project: {model_name}")

    run_dir = _create_run_dir(output_root=output_root, model_name=model_name)
    print(f"Results directory: {run_dir}")

    model = ToyNKModel()
    params = cfg["params"]
    horizon = int(cfg.get("horizon", 40))
    seed = int(cfg.get("seed", 0))

    solver_map = available_solvers()
    requested = cfg.get("solvers", list(solver_map.keys()))

    for solver_name in requested:
        solver = solver_map[solver_name]
        sol = solver.solve(model, params)
        x, _ = simulate_linear_model(sol.F, sol.G, horizon=horizon, seed=seed)

        _save_solver_outputs(
            run_dir=run_dir,
            solver_name=solver_name,
            state_names=model.state_names,
            sol_F=sol.F,
            sol_G=sol.G,
            stable=sol.stable,
            spectral_radius=sol.spectral_radius,
            trajectory=x,
        )

        print("=" * 72)
        print(f"solver: {solver_name}")
        print(f"stable: {sol.stable} | spectral radius: {sol.spectral_radius:.4f}")
        _print_matrix("F", sol.F)
        _print_matrix("G", sol.G)
        print(
            "final state (t=horizon):",
            {k: round(v, 4) for k, v in zip(model.state_names, x[-1], strict=False)},
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run toy DSGE model across solvers")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("src/dsge/configs/toy_nk.yaml"),
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
