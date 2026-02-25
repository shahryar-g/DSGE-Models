from __future__ import annotations

import numpy as np

from dsge.models.nk_model import NKModel
from dsge.solvers.registry import available_solvers


def test_all_solvers_return_close_policy_matrices() -> None:
    params = {
        "sigma": 0.25,
        "kappa": 0.15,
        "a_x": 0.75,
        "a_i": 0.10,
        "b_pi": 0.60,
        "rho_i": 0.70,
        "phi_pi": 1.50,
        "phi_x": 0.30,
        "sd_d": 0.20,
        "sd_c": 0.15,
        "sd_m": 0.10,
    }

    model = NKModel()
    solvers = available_solvers()

    base = solvers["linear_solve"].solve(model, params)

    for name, solver in solvers.items():
        sol = solver.solve(model, params)
        assert np.allclose(sol.F, base.F, atol=1e-10), name
        assert np.allclose(sol.G, base.G, atol=1e-10), name
