from __future__ import annotations

import numpy as np

from dsge.core.interfaces import LinearDSGEModel, LinearSolution, Solver
from dsge.core.simulation import spectral_radius


class DirectInverseSolver(Solver):
    @property
    def name(self) -> str:
        return "direct_inverse"

    def solve(self, model: LinearDSGEModel, params: dict[str, float]) -> LinearSolution:
        H, M, N = model.system_matrices(params)
        H_inv = np.linalg.inv(H)
        F = H_inv @ M
        G = H_inv @ N
        sr = spectral_radius(F)
        return LinearSolution(
            solver_name=self.name,
            F=F,
            G=G,
            stable=sr < 1.0,
            spectral_radius=sr,
        )
