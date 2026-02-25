from __future__ import annotations

import numpy as np

from dsge.core.interfaces import LinearDSGEModel


class RamseyKoopmansModel(LinearDSGEModel):
    """Linearized Ramsey-Koopmans style model in reduced 2-variable form.

    Variables:
      k: log-deviation of capital from steady state
      c: log-deviation of consumption from steady state

    Structural form:
      k_{t+1} = rho_k*k_t - eta_c*c_t + sd_a*e_a
      c_{t+1} = chi_k*k_t + chi_c*c_t + sd_u*e_u

    This compact specification is intended for solver benchmarking in the same
    H E_t[x_{t+1}] = M x_t + N eps_t interface used across the codebase.
    """

    @property
    def state_names(self) -> list[str]:
        return ["k", "c"]

    @property
    def shock_names(self) -> list[str]:
        return ["technology", "preference"]

    def system_matrices(
        self,
        params: dict[str, float],
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        rho_k = params["rho_k"]
        eta_c = params["eta_c"]
        chi_k = params["chi_k"]
        chi_c = params["chi_c"]
        sd_a = params["sd_a"]
        sd_u = params["sd_u"]

        H = np.eye(2, dtype=float)
        M = np.array(
            [
                [rho_k, -eta_c],
                [chi_k, chi_c],
            ],
            dtype=float,
        )
        N = np.diag([sd_a, sd_u]).astype(float)
        return H, M, N
