#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-nk_model}"
CONFIG="src/dsge/configs/${MODEL}.yaml"

if [[ ! -f "$CONFIG" ]]; then
  echo "Config not found: $CONFIG"
  echo "Available configs:"
  ls src/dsge/configs/*.yaml
  exit 1
fi

mkdir -p .mplconfig .cache
export MPLCONFIGDIR="$(pwd)/.mplconfig"
export XDG_CACHE_HOME="$(pwd)/.cache"

python3 -m pip install -q numpy pyyaml matplotlib openpyxl
PYTHONPATH=src python3 -m dsge.experiments.run_model \
  --config "$CONFIG" \
  --output result
