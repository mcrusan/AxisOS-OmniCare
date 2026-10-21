# ==============================================================================
# File: src/omnicare/tentacles/registry.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Decorator-driven registry for OmniCare action tentacles.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Integrated tentacle registry into repo tree.
# ==============================================================================

from typing import Dict, List, Type
from omnicare.tentacles.base import Tentacle

TENTACLE_REGISTRY: Dict[str, Type[Tentacle]] = {}


def register_tentacle(cls: Type[Tentacle]) -> Type[Tentacle]:
    """
    Decorator to register tentacles automatically by `cls.name`.
    """
    TENTACLE_REGISTRY[cls.name] = cls
    return cls


def get_tentacle(name: str) -> Tentacle:
    """
    Retrieve a tentacle instance by name.
    """
    cls = TENTACLE_REGISTRY.get(name)
    if not cls:
        raise ValueError(f"Tentacle '{name}' not found")
    return cls()


def list_tentacles() -> List[str]:
    return sorted(TENTACLE_REGISTRY.keys())
