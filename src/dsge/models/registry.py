from __future__ import annotations

from dsge.core.interfaces import LinearDSGEModel
from dsge.models.nk_model import NKModel
from dsge.models.ramsey_koopmans import RamseyKoopmansModel


def available_models() -> dict[str, LinearDSGEModel]:
    return {
        "nk_model": NKModel(),
        "ramsey_koopmans": RamseyKoopmansModel(),
    }
