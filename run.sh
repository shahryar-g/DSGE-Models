#!/usr/bin/env bash
set -euo pipefail

mkdir -p .mplconfig .cache
export MPLCONFIGDIR="$(pwd)/.mplconfig"
export XDG_CACHE_HOME="$(pwd)/.cache"

python3 -m pip install -q numpy pyyaml matplotlib openpyxl
PYTHONPATH=src python3 -m dsge.experiments.run_nk_model \
  --config src/dsge/configs/nk_model.yaml \
  --output result
