# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Holds common functions used throughout `scripts`"""

from pathlib import Path
import json
import sys


def read_json(source_path: Path):
    """Opens a single json file and returns the contents as a dictionary.

    Parameters
    ----------
    source_path: Path
        The path to the source JSON file.

    Returns
    -------
    dict
        The JSON file contents as a dictionary.
    """
    with open(source_path, 'r') as f:
        dictionary = json.load(f)

    return dictionary
