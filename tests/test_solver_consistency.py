from __future__ import annotations

import numpy as np

from dsge.models.nk_model import NKModel
from dsge.models.ramsey_koopmans import RamseyKoopmansModel
from dsge.solvers.registry import available_solvers


def _assert_solver_consistency(model, params: dict[str, float]) -> None:
    solvers = available_solvers()
    base = solvers["linear_solve"].solve(model, params)

    for name, solver in solvers.items():
        sol = solver.solve(model, params)
        assert np.allclose(sol.F, base.F, atol=1e-10), name
        assert np.allclose(sol.G, base.G, atol=1e-10), name


def test_nk_model_solver_consistency() -> None:
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
    _assert_solver_consistency(NKModel(), params)


def test_ramsey_koopmans_solver_consistency() -> None:
    params = {
        "rho_k": 0.92,
        "eta_c": 0.25,
        "chi_k": 0.08,
        "chi_c": 0.70,
        "sd_a": 0.20,
        "sd_u": 0.12,
    }
    _assert_solver_consistency(RamseyKoopmansModel(), params)
