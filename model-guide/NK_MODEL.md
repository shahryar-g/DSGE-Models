# NK Model Guide

This file documents the included example model in `src/dsge/models/nk_model.py`.

## Variables

- `x`: output gap
- `pi`: inflation
- `i`: nominal interest rate

## Shocks

- demand shock
- cost-push shock
- monetary policy shock

## Structural equations

The model dynamics are:

$$
\begin{aligned}
x_{t+1} - \sigma \pi_{t+1} = a_x x_t - a_i i_t + sd_d e_{d,t}
\\
-\kappa x_{t+1} + \pi_{t+1} = b_\pi \pi_t + sd_c e_{c,t}
\\
i_{t+1} = \rho_i i_t + (1-\rho_i)(\phi_\pi \pi_t + \phi_x x_t) + sd_m e_{m,t}
\end{aligned}
$$

Matrix form used in the code:

$$
H\,\mathbb{E}_t[x_{t+1}] = M x_t + N \varepsilon_t
$$

and the solved transition law:

$$
x_{t+1} = F x_t + G \varepsilon_t
$$

## Parameter source

Baseline calibration is in:

- `src/dsge/configs/nk_model.yaml`
