from __future__ import annotations

import numpy as np

from dsge.core.interfaces import LinearDSGEModel, LinearSolution, Solver
from dsge.core.simulation import spectral_radius


class LinearSolveSolver(Solver):
    @property
    def name(self) -> str:
        return "linear_solve"

    def solve(self, model: LinearDSGEModel, params: dict[str, float]) -> LinearSolution:
        H, M, N = model.system_matrices(params)
        F = np.linalg.solve(H, M)
        G = np.linalg.solve(H, N)
        sr = spectral_radius(F)
        return LinearSolution(
            solver_name=self.name,
            F=F,
            G=G,
            stable=sr < 1.0,
            spectral_radius=sr,
        )
