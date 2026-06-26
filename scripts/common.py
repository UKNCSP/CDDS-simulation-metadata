# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Holds common functions used throughout `scripts`"""

from pathlib import Path
import json
import os

from constants import META_FIELDS


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


def get_issue() -> dict[str, str]:
    """Extracts the issue body from the submitted issue form.

    Returns
    -------
    dict[str, str]
        The issue body as a dictionary.
    """
    return {
        "body": os.environ.get("ISSUE_BODY"),
    }


def process_metadata(match: list) -> dict[str, str]:
    """Generates a dictionary from the loaded issue body and cleans the contents to ensure consistent formatting.

    Parameters
    ----------
    match: list
        The identified key-value pairs from the issue body.

    Returns
    -------
    dict[str, str]
        The dictionary containing the submitted metadata information.
    """
    meta_dict = {}

    # Clean parsed data
    for key, value in set(match):
        clean = key.strip().lower().replace(" ", "_")
        meta_dict[clean] = value.strip()

    # Re map keys to correct CV format
    for old_key, new_key in META_FIELDS.items():
        meta_dict[new_key] = meta_dict.pop(old_key)

    # Reformat blank fields.
    for key, value in meta_dict.items():
        if meta_dict[key] == "_No response_":
            meta_dict[key] = ""

    return meta_dict