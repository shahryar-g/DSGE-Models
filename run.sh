#!/usr/bin/env bash
set -euo pipefail

mkdir -p .mplconfig .cache
export MPLCONFIGDIR="$(pwd)/.mplconfig"
export XDG_CACHE_HOME="$(pwd)/.cache"

python3 -m pip install -q numpy pyyaml matplotlib
PYTHONPATH=src python3 -m dsge.experiments.run_toy_model \
  --config src/dsge/configs/toy_nk.yaml \
  --output result
