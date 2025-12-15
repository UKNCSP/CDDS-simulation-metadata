# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script converts the full mappings.json file into a minimal required information dictionary to save on repository
storage and improve clarity and performance.
"""

import argparse
from pathlib import Path
from typing import Union
import json


def set_arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take source file paths from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.

    """
    parser = argparse.ArgumentParser(description="Open source files")

    mapping_info_description = ("The path to the file containing mapping information associated with each individual"
                                "variable such as the associated title, labels and stash entries."
                                "e.g. reference_information/mappings.json)")
    parser.add_argument("mappings", help=mapping_info_description)

    return parser.parse_args()


def open_source_jsons(path: Path) -> Union[dict, list[dict]]:
    """Opens and reads a single JSON file.

    Parameters
    ----------
    path: Path
        The path of the file to be opened.

    Returns
    -------
    Union[dict, list[dict]]
        The JSON file content.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    json.JSONDecodeError
        If the JSON file structure is invalid.
    """
    try:
        with open(path, "r") as f:
            file = json.load(f)

    except FileNotFoundError:
        print(f"File not found: {path}.")
    except json.JSONDecodeError as err:
        print(f"Invalid JSON formatting: {err}")

    return file


def extract_mapping_information(mapping: dict) -> dict:
    """Returns the title, labels and stash entries (if available) mapping information for a single variable.

    Parameters
    ----------
    mapping: dict
        The dictionary of mapping information for a single variable.

    Returns
    -------
    dict
        The title, labels and stash entries for a single variable.
    """

    return {
        "title": mapping.get("title", ""),
        "labels": mapping.get("labels", []),
        "stash_entries": mapping.get("STASH entries", []),
    }


def main():
    """
    Holds the main body of the script
    """
    args = set_arg_parser()
    mappings_dict = open_source_jsons(Path(args.mappings))

    outdir = Path("reference_information/minimal_mappings.json")

    all_minimal_mappings = []

    for mapping in mappings_dict:
        minimal_mapping = extract_mapping_information(mapping)
        all_minimal_mappings.append(minimal_mapping)

    with open(outdir, "w") as f:
        json.dump(all_minimal_mappings, f, indent=4)


if __name__ == "__main__":
    main()
