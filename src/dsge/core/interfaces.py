from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

Array = np.ndarray


@dataclass
class LinearSolution:
    solver_name: str
    F: Array
    G: Array
    stable: bool
    spectral_radius: float


class LinearDSGEModel(ABC):
    """Interface for models represented as H E_t[x_{t+1}] = M x_t + N eps_t."""

    @property
    @abstractmethod
    def state_names(self) -> list[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def shock_names(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def system_matrices(self, params: dict[str, float]) -> tuple[Array, Array, Array]:
        raise NotImplementedError


class Solver(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def solve(self, model: LinearDSGEModel, params: dict[str, float]) -> LinearSolution:
        raise NotImplementedError
