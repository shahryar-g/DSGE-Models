from __future__ import annotations

from pathlib import Path

from dsge.experiments.run_model import run


if __name__ == "__main__":
    run(config_path=Path("src/dsge/configs/nk_model.yaml"), output_root=Path("result"))
