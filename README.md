# DSGE Solver Lab

A scalable starter codebase for experimenting with DSGE solution methods without restructuring your repository every time your model grows.

## What this repository is for

This project separates concerns so you can iterate fast:

- `models` hold equation systems (`H, M, N`)
- `solvers` hold numerical solution methods (`F, G`)
- `experiments` run and compare results
- `configs` control runs without touching code
- `core` contains common interfaces/utilities

The main design rule is simple:

**If a model returns valid `(H, M, N)`, it can be solved by any registered solver with the same pipeline.**

## How the codebase works

### 1) Interfaces (`src/dsge/core/interfaces.py`)

Two base interfaces define the contract:

- `LinearDSGEModel`
  - `state_names`
  - `shock_names`
  - `system_matrices(params) -> (H, M, N)`
- `Solver`
  - `name`
  - `solve(model, params) -> LinearSolution`

`LinearSolution` is a dataclass carrying:

- `F`, `G`
- `solver_name`
- `stable`
- `spectral_radius`

These interfaces are the key to scalability.

### 2) Model layer (`src/dsge/models/`)

Each model file only does one job: convert parameters into system matrices.

Current included model:

- `toy_nk.py`

Model details are documented separately in:

- [`model-guide/TOY_NK_MODEL.md`](model-guide/TOY_NK_MODEL.md)

### 3) Solver layer (`src/dsge/solvers/`)

Each solver reads `(H, M, N)` and computes reduced-form dynamics `(F, G)`.

Included solvers:

- `direct_inverse.py`
- `linear_solve.py`
- `least_squares.py`

`registry.py` exposes `available_solvers()` so experiments can choose solvers by name from config.

### 4) Experiment layer (`src/dsge/experiments/`)

`run_toy_model.py` is a config-driven runner:

1. Load YAML config
2. Build model
3. Select requested solvers from registry
4. Solve model per solver
5. Simulate paths
6. Print comparable outputs

### 5) Config layer (`src/dsge/configs/`)

`toy_nk.yaml` contains:

- model key
- calibration parameters
- solver list
- simulation horizon/seed

You can change parameters and solver selection without editing Python code.

### 6) Tests (`tests/`)

`test_solver_consistency.py` checks that all included solvers return close `F` and `G` on the baseline config.

## Repository layout

```text
src/dsge/
  core/
    interfaces.py
    simulation.py
  models/
    toy_nk.py
  solvers/
    direct_inverse.py
    linear_solve.py
    least_squares.py
    registry.py
  configs/
    toy_nk.yaml
  experiments/
    run_toy_model.py
tests/
  test_solver_consistency.py
model-guide/
  TOY_NK_MODEL.md
```

## Launch and run

### Fastest run (one command)

```bash
./run.sh
```

This command installs required Python packages (if missing), runs the experiment, and saves outputs automatically.

Results are saved under:

```text
result/<model>/<run_timestamp>/<solver>/
```

Each solver folder contains:

- `F.csv`
- `G.csv`
- `trajectory.csv`
- `states.png`
- `summary.json`

### Manual run (without `run.sh`)

```bash
python3 -m pip install numpy pyyaml matplotlib
PYTHONPATH=src python3 -m dsge.experiments.run_toy_model \
  --config src/dsge/configs/toy_nk.yaml \
  --output result
```

## Run tests

```bash
pip install pytest
PYTHONPATH=src pytest -q
```

## Day-to-day workflow

1. Edit/add model in `src/dsge/models/`
2. Add/update config in `src/dsge/configs/`
3. Run experiment command
4. Compare solver outputs
5. Add tests for new behavior

## Extend without restructuring

### Add a new model

1. Create `src/dsge/models/your_model.py`
2. Implement `LinearDSGEModel`
3. Return `(H, M, N)`
4. Add a YAML config
5. Update experiment model selection (or add model registry)

No solver code changes required.

### Add a new solver

1. Create `src/dsge/solvers/your_solver.py`
2. Implement `Solver`
3. Register it in `src/dsge/solvers/registry.py`
4. Add its name in config under `solvers`

No model code changes required.

## Current status of this starter

- Modular architecture is in place
- Multiple solver backends are wired
- Config-driven run is working
- Baseline consistency test exists

This is intentionally minimal so you can grow it to larger DSGE systems while keeping a stable structure.
