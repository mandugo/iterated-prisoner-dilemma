"""Utility helpers used across the framework."""

from __future__ import annotations

import random
from typing import Optional


def make_rng(seed: Optional[int] = None) -> random.Random:
    """Return a dedicated :class:`random.Random` instance."""

    return random.Random(seed)
