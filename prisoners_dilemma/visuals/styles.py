"""Common Matplotlib styling rules."""

from __future__ import annotations

import contextlib
from typing import Iterator

import matplotlib.pyplot as plt


def apply_default_style() -> None:
    plt.style.use("seaborn-v0_8")


@contextlib.contextmanager
def temporary_style(style: str) -> Iterator[None]:
    original_style = plt.rcParams.copy()
    plt.style.use(style)
    try:
        yield
    finally:
        plt.rcParams.update(original_style)
