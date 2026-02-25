from __future__ import annotations

import numpy as np

from dsge.core.interfaces import LinearDSGEModel


class NKModel(LinearDSGEModel):
    """Small linearized 3-variable New Keynesian-style model.

    Variables: x (output gap), pi (inflation), i (nominal interest rate)

    Structural form:
      x_{t+1} - sigma*pi_{t+1} = a_x*x_t - a_i*i_t + sd_d*e_d
     -kappa*x_{t+1} + pi_{t+1} = b_pi*pi_t + sd_c*e_c
      i_{t+1} = rho_i*i_t + (1-rho_i)*(phi_pi*pi_t + phi_x*x_t) + sd_m*e_m
    """

    @property
    def state_names(self) -> list[str]:
        return ["x", "pi", "i"]

    @property
    def shock_names(self) -> list[str]:
        return ["demand", "cost_push", "monetary"]

    def system_matrices(
        self,
        params: dict[str, float],
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        sigma = params["sigma"]
        kappa = params["kappa"]
        a_x = params["a_x"]
        a_i = params["a_i"]
        b_pi = params["b_pi"]
        rho_i = params["rho_i"]
        phi_pi = params["phi_pi"]
        phi_x = params["phi_x"]
        sd_d = params["sd_d"]
        sd_c = params["sd_c"]
        sd_m = params["sd_m"]

        H = np.array(
            [
                [1.0, -sigma, 0.0],
                [-kappa, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=float,
        )

        M = np.array(
            [
                [a_x, 0.0, -a_i],
                [0.0, b_pi, 0.0],
                [(1.0 - rho_i) * phi_x, (1.0 - rho_i) * phi_pi, rho_i],
            ],
            dtype=float,
        )

        N = np.diag([sd_d, sd_c, sd_m]).astype(float)

        return H, M, N
