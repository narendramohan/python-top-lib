"""Utility functions used throughout the project."""

import os
from pathlib import Path
from typing import Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure that a directory exists.

    Creates the directory and any parents if they do not already exist.

    Args:
        path: Directory path to ensure exists.

    Returns:
        The Path object corresponding to the directory.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p