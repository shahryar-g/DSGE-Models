from __future__ import annotations

import numpy as np


def spectral_radius(matrix: np.ndarray) -> float:
    eigvals = np.linalg.eigvals(matrix)
    return float(np.max(np.abs(eigvals)))


def simulate_linear_model(
    F: np.ndarray,
    G: np.ndarray,
    horizon: int,
    seed: int,
    initial_state: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    n_states = F.shape[0]
    n_shocks = G.shape[1]

    x = np.zeros((horizon + 1, n_states), dtype=float)
    if initial_state is not None:
        x[0] = initial_state

    rng = np.random.default_rng(seed)
    eps = rng.standard_normal(size=(horizon, n_shocks))

    for t in range(horizon):
        x[t + 1] = F @ x[t] + G @ eps[t]

    return x, eps
