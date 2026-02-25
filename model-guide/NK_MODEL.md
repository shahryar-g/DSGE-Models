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

1. IS-type relation

\[
x_{t+1} - \sigma \pi_{t+1} = a_x x_t - a_i i_t + sd_d e_{d,t}
\]

2. Phillips-curve-type relation

\[
-\kappa x_{t+1} + \pi_{t+1} = b_\pi \pi_t + sd_c e_{c,t}
\]

3. Interest-rate rule with smoothing

\[
i_{t+1} = \rho_i i_t + (1-\rho_i)(\phi_\pi \pi_t + \phi_x x_t) + sd_m e_{m,t}
\]

## Parameter source

Baseline calibration is in:

- `src/dsge/configs/nk_model.yaml`
