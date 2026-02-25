from __future__ import annotations

import numpy as np

from dsge.core.interfaces import LinearDSGEModel, LinearSolution, Solver
from dsge.core.simulation import spectral_radius


class LeastSquaresSolver(Solver):
    @property
    def name(self) -> str:
        return "least_squares"

    def solve(self, model: LinearDSGEModel, params: dict[str, float]) -> LinearSolution:
        H, M, N = model.system_matrices(params)
        F = np.linalg.lstsq(H, M, rcond=None)[0]
        G = np.linalg.lstsq(H, N, rcond=None)[0]
        sr = spectral_radius(F)
        return LinearSolution(
            solver_name=self.name,
            F=F,
            G=G,
            stable=sr < 1.0,
            spectral_radius=sr,
        )
