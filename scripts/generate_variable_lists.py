# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the variable lists for each CMIP experiment for each data request version.

This script scans two source files containing CMIP experiments, their associated variables and the variable metadata
such as priority level and production labels. Each varaible is labelled with the required properties and commented as
necessary. Each variable list is then saved to a plain text file containing the variables for that experiment.
"""

import json
import os
import re
from itertools import chain
from pathlib import Path
from typing import Union


def open_source_jsons(path: Path) -> Union[dict, list[dict]]:
    """
    Opens and reads a single JSON file.

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
    PermissionError
        If read access is denied.
    IsADirectoryError
        If given path is a directory and not a file.
    json.JSONDecodeError
        If the JSON file structure is invalid.
    """
    try:
        with open(path, "r") as f:
            file = json.load(f)

    except FileNotFoundError:
        print(f"File not found: {path}.")
    except PermissionError:
        print(f"Read access denied for {path}.")
    except IsADirectoryError:
        print(f"{path} is a directory, not a file.")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON formatting: {e}")

    return file


def get_priority_labels(experiment_dict: dict, experiment: str) -> tuple[dict[str, set], dict[str, str]]:
    """
    Creates a list of variables for each priority group for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    tuple[dict[str, set], dict[str, str]]
        A pair of dictionaries containing the variables with their associated priority and the varaibles with their
        associated label as a result of their priority.
    """
    priority_labels = {}
    experiment_data = experiment_dict["experiment"][experiment]
    priority_dict = {
        "core": set(experiment_data.get("Core", [])),
        "high": set(experiment_data.get("High", [])),
        "med": set(experiment_data.get("Medium", [])),
        "low": set(experiment_data.get("Low", [])),
    }

    for key, value in priority_dict.items():
        if key in ("med", "low"):
            for v in value:
                priority_labels[v] = (f" # priority={'medium' if key == 'med' else 'low'}")

    return priority_dict, priority_labels


def update_variable_priority(experiment_dict: dict, experiment: str, variable_dict: dict) -> dict[str, str]:
    """
    Update the variables for a single experiment with priority comments.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    variable_dict: dict
        An empty dictionary to populate with the updated variable data.

    Returns
    -------
    dict[str, str]
        A dictionary of variable name and priority level key-value pairs for a single experiment.
    """
    priority_dict, priority_labels = get_priority_labels(experiment_dict, experiment)

    # Check all labels against their priority status and label accordingly.
    for variable in chain(priority_dict["core"], priority_dict["high"], priority_dict["med"], priority_dict["low"]):
        priority = priority_labels.get(variable, "")
        variable_dict[variable] = priority

    return variable_dict


def match_variables_with_mappings(mappings_dict: list[dict], variable_dict: dict[str, str]) -> dict[str, str]:
    """
    Verify the production status of each variable for each variable for a single experiment.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.
    ariable_dict: dict[str, str]
        The dictionary of name and priority level key-value pairs for a single experiment.

    Returns
    -------
    dict[str, str]
        An updated dictionary containing production status for variables marked "do-not-produce".
    """
    # Loop over all variables to find those labelled as "do-not-produce" and mark them as such.
    for map in mappings_dict:
        title = map.get("title", "")
        labels = map.get("labels", [])
        variable = re.search(r"Variable\s+([^\s(]+)", title).group(1)

        # Overriding any existing "priority" value in the dict is acceptable since do-not-produce takes precedence.
        if "do-not-produce" in labels:
            variable_dict[variable] = " # do-not-produce"

    return variable_dict


def get_variable_streams(mappings_dict: list[dict]) -> dict[str, str]:
    """
    Creates a dictionary for variables and their associated output stream.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.

    Returns
    -------
    dict[str, str]
        A dictionary containing variables and their associated output stream.
    """
    streams = {}

    # Access stash entries for each variable and check if it contains values.
    for map in mappings_dict:
        title = map.get("title", "")
        stream = ""
        variable = re.search(r"Variable\s+([^\s(]+)", title).group(1)
        stash_entries = map.get("STASH entries", [])

        # If stash entries contains any values get the usage profile.
        if stash_entries:
            usage_profile = stash_entries[0].get("usage_profile", "")
            # Map usage profile to stream.
            stream = usage_profile.replace("UP", "ap") if usage_profile else ""
        # Create a local dictionary to pair variables and their streams.
        streams[variable] = stream

    return streams


def reformat_varaible_names(mappings_dict: list[dict], variable_dict: dict) -> dict[str, str]:
    """
    Reformats the name of each variable from realm.variable.branding.frequency.region to
    realm/variable_branding@frequency:stream for a single experiment.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.
    variable_dict: dict
        An updated dictionary containing production status for variables marked "do-not-produce".

    Returns
    -------
    dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production status as
        values.

    Raises
    ------
    KeyError
        If the original variable name cannot be split into parts as expected.
    """
    renamed_variable_dict = {}
    streams = get_variable_streams(mappings_dict)

    # Reformat all original variable names to realm/variable_branding@frequency:stream.
    for key, value in variable_dict.items():
        parts = key.split(".")
        if len(parts) < 4:
            raise KeyError(f"{key} has unexpected format. Expected: realm.variable.branding.frequency.region")

        realm, variable, branding, frequency = parts[:4]
        stream = streams.get(key, "")
        var_with_stream = f"{realm}/{variable}_{branding}@{frequency}:{stream}"
        var_without_stream = f"{realm}/{variable}_{branding}@{frequency}"

        # Create new dictionary with the reformatted variable names to avoid key errors in the original dict.
        new_varaible_name = var_with_stream if stream else var_without_stream
        renamed_variable_dict[new_varaible_name] = value

    return renamed_variable_dict


def format_outfile_content(renamed_variable_dict: dict[str, str]) -> list[str]:
    """
    Reformats the key value pairs into single line plain text for a single experiment.

    Parameters
    ----------
    renamed_variable_dict: dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production status as
        values.

    Returns
    -------
    list[str]
        A list of lines to populate the plain text file with.
    """
    lines = []
    for key, value in renamed_variable_dict.items():
        if value:
            line = f"#{key}{value}\n"
        else:
            line = f"{key}{value}\n"
        lines.append(line)

    return lines


def sorted_lines(lines: list[str]) -> list[str]:
    """
    Sorts the variables for a single experiment in order of priority.

    Parameters
    ----------
    lines: list[str]
        The unordered variables with the appropriate comments.

    Returns
    -------
    list[str]
        A list of sorted variables with the appropriate comments in order of priority.
    """
    order = {"# priority=medium": 1, "# priority=low": 2, "# do-not-produce": 3}
    filtered_lines = []

    for line in set(lines):
        if not line.startswith("#") or any(name in line for name in order):
            filtered_lines.append(line)

    sorted_lines = sorted(
        filtered_lines,
        key=lambda line: order.get(next((name for name in order if name in line), None), 0),
    )

    return sorted_lines


def save_file(outdir: Path, experiment: str, variable_dict: dict[str, str]) -> None:
    """
    Saves a single file to a plain text format.

    Parameters
    ----------
    outdir: Path
        The output directory.
    experiment: str
        The experiment whose variables are being saved.
    variable_dict: dict[str, str]
        The final dictionary containing the reformatted variable names as keys and priority/production status as values.
    """
    outfile = outdir / f"{experiment}.txt"
    with open(outfile, "w") as f:
        for line in sorted_lines(format_outfile_content(variable_dict)):
            f.write(line)


def generate_variable_lists() -> None:
    """
    Generates the variable list files for all experiments.
    """
    # Call required source files.
    experiment_dict = open_source_jsons(Path("reference_information/dr-1.2.2.2_all.json"))
    mappings_dict = open_source_jsons(Path("reference_information/mappings.json"))

    # Create output file path.
    outdir = Path(f"variables/{experiment_dict['Header']['dreq content version']}")
    os.makedirs(outdir, exist_ok=True)

    # Loop over all listed experiments.
    for experiment in experiment_dict["experiment"]:
        variable_dict = {}
        functions = [
            update_variable_priority(experiment_dict, experiment, variable_dict),
            match_variables_with_mappings(mappings_dict, variable_dict),
            reformat_varaible_names(mappings_dict, variable_dict),
        ]
        for f in functions:
            variable_dict = f

        save_file(outdir, experiment, variable_dict)

    print(f"SUCCESSFULLY GENERATED {len(experiment_dict['experiment'])} FILES")


if __name__ == "__main__":
    generate_variable_lists()
