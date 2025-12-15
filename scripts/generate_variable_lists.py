# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the variable lists for each CMIP experiment for each data request version.

This script scans two source files containing CMIP experiments, their associated variables and the variable metadata
such as priority level and production labels. Each variable is labelled accordingly and commented out as necessary.
Each variable list is then saved to a plain text file containing the variables for that experiment.
"""

import json
import os
import re
from itertools import chain
from pathlib import Path
from typing import Union
import argparse

IGNORED_PRIORITIES = ("med", "low")
PRIORITY_ORDER = {"# priority=medium": 1, "# priority=low": 2, "# do-not-produce": 3}


def set_arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take source file paths from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.

    """
    parser = argparse.ArgumentParser(description="Open source files")

    experiment_info_description = ("The path to the file containing all included experiemnts and their associated"
                                   "variables grouped by priority e.g. reference_information/dr-1.2.2.2_all.json")
    parser.add_argument("experiments", help=experiment_info_description)

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
        "labels": mapping.get("labels", []),
        "stash_entries": mapping.get("STASH entries", []),
        "title": mapping.get("title", ""),
    }


def get_grouped_priority_labels(experiment_dict: dict, experiment: str) -> dict[str, set]:
    """Creates a dictionary of labels grouped by priority (core, high, med, low) for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    dict[str, set]
        A dictionary of labels grouped by priority (core, high, med, low).
    """
    experiment_data = experiment_dict["experiment"][experiment]

    return {
        "core": set(experiment_data.get("Core", [])),
        "high": set(experiment_data.get("High", [])),
        "med": set(experiment_data.get("Medium", [])),
        "low": set(experiment_data.get("Low", [])),
    }


def set_priority_comments(experiment_dict: dict, experiment: str) -> dict[str, str]:
    """Sets the comment to be appended to each variable based off of their priority level for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    dict[str, str]
        A dictionary of comments created based on priority level.
    """
    priority_comments = {}
    priority_dict = get_grouped_priority_labels(experiment_dict, experiment)
    for level, variables in priority_dict.items():
        if level in IGNORED_PRIORITIES:
            for variable in variables:
                priority_comments[variable] = f" # priority={'medium' if level == 'med' else 'low'}"

    return priority_comments


def get_all_variables(experiment_dict: dict, experiment: str) -> chain:
    """Creates a chain of all variables used for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    chain
        A chain of all priority labels.
    """
    priority_dict = get_grouped_priority_labels(experiment_dict, experiment)

    return chain(priority_dict["core"], priority_dict["high"], priority_dict["med"], priority_dict["low"])


def update_variables_with_priority(experiment_dict: dict, experiment: str, variable_dict: dict) -> dict[str, str]:
    """Update the variables for a single experiment with priority comments.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    variable_dict: dict
        A dictionary to populate with the updated variable data.

    Returns
    -------
    dict[str, str]
        A dictionary of variable name and priority level key-value pairs for a single experiment.
    """
    priority_comments = set_priority_comments(experiment_dict, experiment)
    all_labels = get_all_variables(experiment_dict, experiment)

    # Check all labels against their priority status and label accordingly.
    for variable in all_labels:
        comment = priority_comments.get(variable, "")
        variable_dict[variable] = comment

    return variable_dict


def extract_variable_from_title(mapping: dict) -> str:
    """Returns the variable name from the given title within the mapping dictionary for a single variable.

    Parameters
    ----------
    mapping: dict
        The mapping dictionary for a single variable.

    Returns
    -------
    str
        The variable name.
    """
    title = extract_mapping_information(mapping)["title"]

    return re.search(r"Variable\s+([^\s(]+)", title).group(1)


def identify_not_produced(mappings_dict: list[dict], variable_dict: dict[str, str]) -> dict[str, str]:
    """Identify all variables marked as "do not produce" in a single experiment.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.
    variable_dict: dict[str, str]
        The dictionary of name and priority level key-value pairs for a single experiment.

    Returns
    -------
    dict[str, str]
        An updated dictionary containing production status for variables marked "do-not-produce".
    """
    # Loop over all variables to find those labelled as "do-not-produce" and mark them as such.
    for mapping in mappings_dict:
        labels = extract_mapping_information(mapping)["labels"]
        variable = extract_variable_from_title(mapping)

        # Overriding any existing "priority" value in the dict is acceptable since do-not-produce takes precedence.
        if "do-not-produce" in labels:
            variable_dict[variable] = " # do-not-produce"

    return variable_dict


def get_streams(mappings_dict: list[dict]) -> dict[str, str]:
    """Creates a dictionary for variables and their associated output stream for a single experiment.

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
    for mapping in mappings_dict:
        variable = extract_variable_from_title(mapping)
        stash_entries = extract_mapping_information(mapping)["stash_entries"]
        stream = ""

        # If stash entries contains any values get the usage profile.
        if stash_entries:
            usage_profile = stash_entries[0].get("usage_profile", "")
            # Map usage profile to stream.
            stream = usage_profile.replace("UP", "ap") if usage_profile else ""

        streams[variable] = stream

    return streams


def reformat_variable_names(mappings_dict: list[dict], variable_dict: dict) -> dict[str, str]:
    """Reformats the name of each variable from realm.variable.branding.frequency.region to
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
    streams = get_streams(mappings_dict)

    # Reformat all original variable names to realm/variable_branding@frequency:stream.
    for variable, comment in variable_dict.items():
        parts = variable.split(".")
        if len(parts) < 4:
            raise KeyError(f"{variable} has unexpected format. Expected: realm.variable.branding.frequency.region")

        realm, variable_name, branding, frequency = parts[:4]
        stream = streams.get(variable, "")
        var_with_stream = f"{realm}/{variable_name}_{branding}@{frequency}:{stream}"
        var_without_stream = f"{realm}/{variable_name}_{branding}@{frequency}"

        # Create new dictionary with the reformatted variable names to avoid key errors in the original dict.
        new_variable_name = var_with_stream if stream else var_without_stream
        renamed_variable_dict[new_variable_name] = comment

    return renamed_variable_dict


def format_outfile_content(renamed_variable_dict: dict[str, str]) -> list[str]:
    """Reformats the key value pairs into single line plain text for a single experiment.

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
    for variable, comment in renamed_variable_dict.items():
        line = f"#{variable}{comment}\n" if comment else f"{variable}{comment}\n"
        lines.append(line)

    return lines


def sort_key(line: str) -> tuple[dict[str, int], int]:
    """The custom sort function passed to the sorted() function to define the variable order for a single experiment.

    Parameters
    ----------
    line: str
        A single line containing a single variable name and associated comments.

    Returns
    -------
    tuple[dict[str, int], int]
        The order of each label based on priority, variables with no specified priority will be assigned order 0 so that
        they appear at the top of the variable list.
    """
    for label in PRIORITY_ORDER:
        if label in line:
            return PRIORITY_ORDER[label]

    return 0


def save_outfile(outdir: Path, experiment: str, renamed_variable_dict: dict[str, str]) -> None:
    """Saves a single file to a plain text format.

    Parameters
    ----------
    outdir: Path
        The output directory.
    experiment: str
        The experiment whose variables are being saved.
    renamed_variable_dict: dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production status as
        values.
    """
    outfile = outdir / f"{experiment}.txt"
    lines = format_outfile_content(renamed_variable_dict)

    with open(outfile, "w") as f:
        for line in sorted(lines, key=sort_key):
            f.write(line)


def generate_variable_lists() -> None:
    """
    Generates the variable list files for all experiments.
    """
    # Call required source files.
    args = set_arg_parser()
    experiment_dict = open_source_jsons(Path(args.experiments))
    mappings_dict = open_source_jsons(Path(args.mappings))

    # Create output file path.
    outdir = Path(f"variables/{experiment_dict['Header']['dreq content version']}")
    os.makedirs(outdir, exist_ok=True)

    # Loop over all listed experiments.
    for experiment in experiment_dict["experiment"]:
        variable_dict = {}

        functions = [
            update_variables_with_priority(experiment_dict, experiment, variable_dict),
            identify_not_produced(mappings_dict, variable_dict),
            reformat_variable_names(mappings_dict, variable_dict),
        ]
        for f in functions:
            variable_dict = f

        save_outfile(outdir, experiment, variable_dict)

    print(f"SUCCESSFULLY GENERATED {len(experiment_dict['experiment'])} FILES")


if __name__ == "__main__":
    generate_variable_lists()
