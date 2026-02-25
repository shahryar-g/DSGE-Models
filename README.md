# DSGE Solver Lab

A scalable starter codebase for DSGE experiments where you can increase model complexity without changing repository structure.

## Codebase overview

- `src/dsge/core/`: interfaces and shared simulation helpers
- `src/dsge/models/`: model definitions (currently `nk_model.py`)
- `src/dsge/solvers/`: interchangeable solver backends
- `src/dsge/configs/`: run/calibration configs
- `src/dsge/experiments/`: experiment runners
- `tests/`: consistency checks
- `model-guide/`: model-specific economic documentation

Core contract:

- A model returns `(H, M, N)`.
- Any registered solver can solve it and produce `(F, G)`.
- The experiment runner handles simulation and outputs.

## Fastest run

```bash
cd /path/to/DSGE-Models
./run.sh
```

## Output structure

Each run saves to:

```text
result/nk_model/<run_timestamp>/
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
PYTHONPATH=src python3 -m dsge.experiments.run_nk_model \
  --config src/dsge/configs/nk_model.yaml \
  --output result
```

## Main files

- `src/dsge/models/nk_model.py`
- `src/dsge/experiments/run_nk_model.py`
- `src/dsge/configs/nk_model.yaml`
- `run.sh`

Model details are documented in:

- `model-guide/NK_MODEL.md`
