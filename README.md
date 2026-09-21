# DSGE Solver Lab

A small Python framework for comparing solution methods for linearized DSGE models. Models and solvers plug into a shared matrix interface, so you can add a new model or a new solver without changing the rest of the code.

## Models

| Model | Variables | Guide |
|---|---|---|
| `nk_model` | Output gap, inflation, interest rate (New Keynesian, with interest-rate smoothing) | [NK_MODEL.md](model-guide/NK_MODEL.md) |
| `ramsey_koopmans` | Capital, consumption (Ramsey-Koopmans with Euler-type dynamics) | [RAMSEY_KOOPMANS_MODEL.md](model-guide/RAMSEY_KOOPMANS_MODEL.md) |

## Solvers

Every registered solver is run on the same model, and the results are compared:

- `linear_solve`
- `direct_inverse`
- `least_squares`

## How it works

- A model returns the matrices `(H, M, N)`.
- Any registered solver takes them and produces the policy matrices `(F, G)`.
- The generic experiment runner then simulates the model and saves the outputs.

## Quick start

Requires Python 3.10+.

```bash
./run.sh                  # runs nk_model by default
./run.sh ramsey_koopmans  # pick a model explicitly
```

`run.sh` installs the dependencies (numpy, pyyaml, matplotlib, openpyxl) and runs the experiment. To run it by hand:

```bash
pip install numpy pyyaml matplotlib openpyxl
PYTHONPATH=src python3 -m dsge.experiments.run_model \
  --config src/dsge/configs/nk_model.yaml \
  --output result
```

Calibrations and simulation settings (horizon, shock size, seed, parameters) live in the YAML files in `src/dsge/configs/`.

## Output

Each run writes to `result/<model>/<run_timestamp>/`:

- `timeseries.xlsx`: one sheet per solver, with time and state values
- `<solver>/irf/irf_matrix.png`: impulse responses (variables x shocks)
- `<solver>/steady_state/states_vs_steady.png`: state paths against steady-state levels

## Tests

```bash
PYTHONPATH=src python3 -m pytest tests
```

Checks that all solvers agree on both models.

## Repository layout

```text
src/dsge/
  core/          interfaces and shared simulation helpers
  models/        model definitions and registry
  solvers/       solver backends and registry
  configs/       run and calibration configs (YAML)
  experiments/   generic experiment runner
tests/           solver consistency checks
model-guide/     economic documentation for each model
run/             model-specific launch scripts
```

## Adding a model or solver

1. Add a model class under `src/dsge/models/` and register it in `registry.py`.
2. Add a config in `src/dsge/configs/<model>.yaml`.
3. For a new solver, add it under `src/dsge/solvers/` and register it in `registry.py`. It will then be included in every run automatically.
