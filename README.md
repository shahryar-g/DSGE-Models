# DSGE Solver Lab

A minimal but scalable framework for building, solving, and comparing linearized DSGE models with multiple numerical solvers.

This repository is designed for one core goal: **you can increase model size/complexity without changing the repository architecture**.

## Why this setup

When DSGE projects grow, codebases often become hard to maintain because model equations, solver logic, simulation code, and experiments are tightly coupled. This template separates these concerns:

- Models define economics (`H, M, N` matrices).
- Solvers define numerical methods (`F, G` solution matrices).
- Experiments run comparisons and simulations.
- Config files hold parameterization.

That separation lets you swap model and solver independently.

## Mathematical setup

The framework uses this linear rational-expectations-style representation:

\[
H \; E_t[x_{t+1}] = M \; x_t + N \; \varepsilon_t
\]

Where:

- `x_t` is the vector of endogenous state/control variables.
- `\varepsilon_t` is the vector of exogenous shocks.
- `H, M, N` are model-implied coefficient matrices.

Given `(H, M, N)`, each solver computes reduced-form transition equations:

\[
x_{t+1} = F x_t + G \varepsilon_t
\]

with:

- `F` governing endogenous dynamics.
- `G` mapping shocks into the system.

In this starter project, solvers differ computationally, but target the same mathematical object.

## Included toy model (New Keynesian style)

File: `src/dsge/models/toy_nk.py`

Variables:

- `x`: output gap
- `pi`: inflation
- `i`: nominal interest rate

Shocks:

- demand shock
- cost-push shock
- monetary policy shock

Structural equations implemented in the model:

1. IS-type relation:
\[
x_{t+1} - \sigma \pi_{t+1} = a_x x_t - a_i i_t + sd_d e_{d,t}
\]

2. Phillips-curve-type relation:
\[
-\kappa x_{t+1} + \pi_{t+1} = b_\pi \pi_t + sd_c e_{c,t}
\]

3. Interest-rate rule with smoothing:
\[
i_{t+1} = \rho_i i_t + (1-\rho_i)(\phi_\pi \pi_t + \phi_x x_t) + sd_m e_{m,t}
\]

These equations are converted into the matrix triplet `(H, M, N)` returned by `system_matrices(params)`.

## Solvers included

All solvers implement the same interface in `src/dsge/core/interfaces.py` and return:

- `F`, `G`
- stability flag
- spectral radius of `F`

### 1) `direct_inverse`

File: `src/dsge/solvers/direct_inverse.py`

Method:

- Computes `H^{-1}` explicitly.
- Uses `F = H^{-1}M`, `G = H^{-1}N`.

Pros:

- Conceptually direct.

Cons:

- Explicit inverse can be less numerically robust for large/ill-conditioned systems.

### 2) `linear_solve`

File: `src/dsge/solvers/linear_solve.py`

Method:

- Solves linear systems directly: `HF=M` and `HG=N` via `np.linalg.solve`.

Pros:

- Usually preferred over explicit inverse for numerical stability.

Cons:

- Requires nonsingular `H`.

### 3) `least_squares`

File: `src/dsge/solvers/least_squares.py`

Method:

- Uses least-squares solution for `HF≈M`, `HG≈N` with `np.linalg.lstsq`.

Pros:

- Works as a fallback when `H` is singular or nearly singular.

Cons:

- May produce approximate solutions not equivalent to exact inversion.

## Stability check

After solving, the code computes the spectral radius:

\[
\rho(F) = \max_i |\lambda_i(F)|
\]

A simple stability flag is defined as `rho(F) < 1`.

This is a practical first diagnostic for explosive dynamics. For advanced DSGE use, you can later add stricter existence/uniqueness diagnostics (e.g., generalized Schur / Blanchard-Kahn checks).

## Repository structure

```text
src/dsge/
  core/
    interfaces.py      # model/solver interfaces + LinearSolution
    simulation.py      # simulation + spectral radius helper
  models/
    toy_nk.py          # example DSGE model
  solvers/
    direct_inverse.py
    linear_solve.py
    least_squares.py
    registry.py        # solver factory/registry
  configs/
    toy_nk.yaml        # baseline parameters + selected solvers
  experiments/
    run_toy_model.py   # config-driven experiment runner
tests/
  test_solver_consistency.py
```

## Quick start

### 1) Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Run the experiment

```bash
python -m dsge.experiments.run_toy_model --config src/dsge/configs/toy_nk.yaml
```

The script prints, for each solver:

- stability and spectral radius
- solved `F` and `G`
- final simulated state at the chosen horizon

### 3) (Optional) run tests

```bash
pip install pytest
PYTHONPATH=src pytest -q
```

## How to add a new model (scalable path)

1. Create a new file in `src/dsge/models/`.
2. Implement `LinearDSGEModel`:
   - `state_names`
   - `shock_names`
   - `system_matrices(params) -> (H, M, N)`
3. Add a YAML config in `src/dsge/configs/`.
4. Update experiment selection logic (or generalize model registry).
5. Reuse existing solvers without rewriting solver code.

The key scalability contract is: **as long as your model returns valid `(H, M, N)`, the rest of the pipeline stays unchanged**.

## How to add a new solver

1. Add a new solver class in `src/dsge/solvers/` implementing `Solver`.
2. Return a `LinearSolution` object.
3. Register it in `src/dsge/solvers/registry.py`.
4. Add the solver name in config under `solvers:`.

No model code changes are needed when adding solvers.

## Current limitations (intentional for v0)

- Only one included model (`toy_nk`).
- No estimation/inference layer yet.
- No IRF plotting yet.
- No generalized eigenvalue (QZ) solver yet.

This is intentional: keep v0 small, modular, and easy to extend.

## Suggested roadmap

1. Add model registry to run multiple model classes from config.
2. Add IRF and moments module.
3. Add SciPy/QZ-based solver and Blanchard-Kahn diagnostics.
4. Add calibration/estimation workflow.
5. Add CI test matrix for multiple Python versions.

## License

Choose your preferred license before publishing (MIT is common for research tooling).
