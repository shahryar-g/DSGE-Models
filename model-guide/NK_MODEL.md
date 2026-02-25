# NK Model Guide

This note documents the baseline New Keynesian (NK) linear model implemented in `src/dsge/models/nk_model.py`.

## 1. Scope and interpretation

The implemented system is a compact linearized NK-style model designed for computational benchmarking across solver backends. It is intentionally small, but preserves the main structural channels of modern monetary DSGE models:

- aggregate demand (IS relation),
- aggregate supply (Phillips relation),
- monetary policy feedback with interest-rate smoothing.

The model is specified in linear state-space form and solved under rational expectations in reduced-form transition form.

## 2. Endogenous variables and shocks

Let

$$
x_t = \begin{bmatrix}
\tilde y_t \\
\pi_t \\
i_t
\end{bmatrix},
$$

where:

- $\tilde y_t$ is the output gap,
- $\pi_t$ is inflation,
- $i_t$ is the nominal policy rate.

The structural innovations are

$$
\varepsilon_t = \begin{bmatrix}
e^d_t \\
e^c_t \\
e^m_t
\end{bmatrix},
$$

where $e^d_t$ is a demand disturbance, $e^c_t$ is a cost-push disturbance, and $e^m_t$ is a monetary-policy disturbance.

## 3. Structural equations

The model dynamics are:

$$
\begin{aligned}
\tilde y_{t+1} - \sigma \pi_{t+1}
&= a_x\tilde y_t - a_i i_t + sd_d\,e^d_t, \\
-\kappa \tilde y_{t+1} + \pi_{t+1}
&= b_\pi \pi_t + sd_c\,e^c_t, \\
i_{t+1}
&= \rho_i i_t + (1-\rho_i)(\phi_\pi \pi_t + \phi_x \tilde y_t) + sd_m\,e^m_t.
\end{aligned}
$$

### 3.1 Economic interpretation

1. Intertemporal demand block (IS-type equation):
- Higher current policy rates ($i_t$) reduce next-period demand through $a_i>0$.
- Expected inflation enters with loading $\sigma$, capturing real-rate effects in reduced-form linearized form.

2. Supply block (Phillips-type equation):
- Marginal-cost/output-gap pressure transmits through $\kappa$.
- Inflation persistence is captured by $b_\pi$ in this compact representation.

3. Monetary policy rule:
- Interest-rate smoothing is governed by $\rho_i \in [0,1)$.
- Contemporaneous policy feedback to inflation and activity is governed by $(\phi_\pi,\phi_x)$.

## 4. Matrix representation used in the code

The implementation maps the system into:

$$
H\,\mathbb E_t[x_{t+1}] = Mx_t + N\varepsilon_t.
$$

With variable ordering $(\tilde y_t,\pi_t,i_t)'$, the matrices are:

$$
H =
\begin{bmatrix}
1 & -\sigma & 0 \\
-\kappa & 1 & 0 \\
0 & 0 & 1
\end{bmatrix},
\qquad
M =
\begin{bmatrix}
a_x & 0 & -a_i \\
0 & b_\pi & 0 \\
(1-\rho_i)\phi_x & (1-\rho_i)\phi_\pi & \rho_i
\end{bmatrix},
$$

$$
N =
\begin{bmatrix}
sd_d & 0 & 0 \\
0 & sd_c & 0 \\
0 & 0 & sd_m
\end{bmatrix}.
$$

This is exactly the contract returned by `system_matrices(params)` in the model class.

## 5. Reduced-form solution

Solvers in `src/dsge/solvers/` compute the reduced form:

$$
x_{t+1} = Fx_t + G\varepsilon_t,
$$

where, in the nonsingular benchmark case,

$$
F = H^{-1}M,
\qquad
G = H^{-1}N.
$$

Different solver modules differ numerically (direct inverse, linear solve, least squares fallback), but target the same $(F,G)$ mapping.

## 6. Stability diagnostic

The code reports the spectral radius:

$$
\rho(F)=\max_j |\lambda_j(F)|.
$$

A practical local stability indicator is $\rho(F)<1$, implying mean-reverting transition dynamics in the simulated linear system.

## 7. Calibration and configuration

Baseline calibration is defined in:

- `src/dsge/configs/nk_model.yaml`

That file contains:

- structural coefficients,
- shock scales,
- simulation horizon,
- IRF horizon and shock size,
- steady-state reference values used in plotting.

## 8. Intended use in this repository

This NK specification is a baseline benchmark for solver comparison and pipeline validation. It is intentionally simple so you can:

- replace or expand the model block while keeping the same `(H,M,N)` interface,
- evaluate solver robustness as dimensionality grows,
- retain unchanged experiment/output tooling.

In that sense, the model is both an economic template and a software-integration testbed for larger DSGE development.
