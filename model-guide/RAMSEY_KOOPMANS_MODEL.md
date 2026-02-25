# Ramsey-Koopmans Model Guide

This note documents the baseline Ramsey-Koopmans style model implemented in `src/dsge/models/ramsey_koopmans.py`.

## 1. Scope

The implementation is a compact linearized benchmark with capital accumulation and Euler-type consumption dynamics. It is designed for solver benchmarking in the same matrix interface used across the repository.

## 2. Variables and shocks

State vector:

$$
x_t = \begin{bmatrix} k_t \\ c_t \end{bmatrix}
$$

where:

- $k_t$: log-deviation of capital from steady state,
- $c_t$: log-deviation of consumption from steady state.

Shock vector:

$$
\varepsilon_t = \begin{bmatrix} e^a_t \\ e^u_t \end{bmatrix}
$$

where:

- $e^a_t$: technology disturbance,
- $e^u_t$: preference disturbance.

## 3. Structural form

$$
\begin{aligned}
k_{t+1} &= \rho_k k_t - \eta_c c_t + sd_a\,e^a_t, \\
c_{t+1} &= \chi_k k_t + \chi_c c_t + sd_u\,e^u_t.
\end{aligned}
$$

Interpretation:

- $\rho_k$ captures persistence of capital deviations,
- $\eta_c$ reflects resource-pressure effect of consumption on future capital,
- $(\chi_k,\chi_c)$ summarize linearized Euler/transition feedback in reduced form.

## 4. Matrix representation

The model is written as:

$$
H\,\mathbb E_t[x_{t+1}] = Mx_t + N\varepsilon_t
$$

with:

$$
H = I_2,
\quad
M = \begin{bmatrix}
\rho_k & -\eta_c \\
\chi_k & \chi_c
\end{bmatrix},
\quad
N = \begin{bmatrix}
sd_a & 0 \\
0 & sd_u
\end{bmatrix}.
$$

## 5. Reduced form and solution

Solvers compute:

$$
x_{t+1} = Fx_t + G\varepsilon_t,
$$

and with $H=I_2$, the benchmark solution is $F=M$ and $G=N$.

## 6. Calibration file

Baseline calibration is in:

- `src/dsge/configs/ramsey_koopmans.yaml`
