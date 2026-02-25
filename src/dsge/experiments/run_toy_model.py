from __future__ import annotations

import argparse
from pathlib import Path

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


def run(config_path: Path) -> None:
    cfg = _load_config(config_path)
    model_name = cfg["model"]
    if model_name != "toy_nk":
        raise ValueError(f"Unsupported model in this starter project: {model_name}")

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

        print("=" * 72)
        print(f"solver: {solver_name}")
        print(f"stable: {sol.stable} | spectral radius: {sol.spectral_radius:.4f}")
        _print_matrix("F", sol.F)
        _print_matrix("G", sol.G)
        print(
            "final state (t=horizon):",
            {k: round(v, 4) for k, v in zip(model.state_names, x[-1])},
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run toy DSGE model across solvers")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("src/dsge/configs/toy_nk.yaml"),
        help="Path to YAML config",
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
