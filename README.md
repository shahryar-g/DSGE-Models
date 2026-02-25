# DSGE Solver Lab

A scalable starter codebase for DSGE experiments where you can increase model complexity without changing repository structure.

## Codebase overview

- `src/dsge/core/`: interfaces and shared simulation helpers
- `src/dsge/models/`: model definitions (`nk_model.py`, `ramsey_koopmans.py`)
- `src/dsge/solvers/`: interchangeable solver backends
- `src/dsge/configs/`: run/calibration configs
- `src/dsge/experiments/`: generic experiment runner
- `tests/`: solver consistency checks
- `model-guide/`: model-specific economic documentation
- `run/`: model-specific launch scripts

Core contract:

- A model returns `(H, M, N)`.
- Any registered solver can solve it and produce `(F, G)`.
- The generic experiment runner handles simulation and outputs.

## Fastest run

Default model (`nk_model`):

```bash
./run.sh
```

Choose model explicitly:

```bash
./run.sh nk_model
./run.sh ramsey_koopmans
```

Or use model-specific scripts:

```bash
./run/run_nk_model.sh
./run/run_ramsey_koopmans.sh
```

## Output structure

Each run saves to:

```text
result/<model>/<run_timestamp>/
```

Inside each solver folder, only these plots are saved:

- `irf/irf_matrix.png` (variables x shocks IRF matrix)
- `steady_state/states_vs_steady.png` (state paths with steady-state levels)

At the run root, one Excel file is saved:

- `timeseries.xlsx`

`timeseries.xlsx` contains one sheet per solver, with time and state values.

## Manual run

```bash
python3 -m pip install numpy pyyaml matplotlib openpyxl
PYTHONPATH=src python3 -m dsge.experiments.run_model \
  --config src/dsge/configs/nk_model.yaml \
  --output result
```

Use `src/dsge/configs/ramsey_koopmans.yaml` to run the Ramsey-Koopmans model.

## Main files

- `src/dsge/experiments/run_model.py`
- `src/dsge/models/nk_model.py`
- `src/dsge/models/ramsey_koopmans.py`
- `src/dsge/configs/nk_model.yaml`
- `src/dsge/configs/ramsey_koopmans.yaml`
- `run.sh`
- `run/run_nk_model.sh`
- `run/run_ramsey_koopmans.sh`

Model details are documented in:

- `model-guide/NK_MODEL.md`
- `model-guide/RAMSEY_KOOPMANS_MODEL.md`
