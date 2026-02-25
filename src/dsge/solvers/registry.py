from __future__ import annotations

from dsge.core.interfaces import Solver
from dsge.solvers.direct_inverse import DirectInverseSolver
from dsge.solvers.least_squares import LeastSquaresSolver
from dsge.solvers.linear_solve import LinearSolveSolver


def available_solvers() -> dict[str, Solver]:
    solvers = [
        DirectInverseSolver(),
        LinearSolveSolver(),
        LeastSquaresSolver(),
    ]
    return {solver.name: solver for solver in solvers}
