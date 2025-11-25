# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the lists for each CMIP experiment for each data request version.
"""

import json
import os
import re
from itertools import chain
from pathlib import Path
from typing import Any, Union

from tqdm import tqdm


def open_source_jsons(path: Path) -> Union[dict[str], list[dict[str]]]:
    """
    Opens and reads a single JSON file.

        :param path: The path of the file to be opened.
        :returns: The JSON file content.
        :raises FileNotFoundError: If the file does not exist at the given path.
        :raises PermissionError: If read access is denied.
        :raises IsADirectoryError: If given path is a directory and not a file.
        :raises json.JSONDecodeError: If the JSON file structure is invalid.
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


def get_priority_labels(experiment_dict: dict[Any], experiment: str) -> list[str]:
    """
    Creates a list of variables for each priority group for a single experiment.

        :param experiment_dict: The dictionary containing all experiments and their associated variables.
        :param experiment: The experiment whose variables are being updated.
        :returns: A list of variables for each priority group
        :raises KeyError: If a required key does not exist.
    """
    try:
        exp_data = experiment_dict["experiment"][experiment]

        return (
            exp_data.get("Core", []),
            exp_data.get("High", []),
            exp_data.get("Medium", []),
            exp_data.get("Low", []),
        )

    except KeyError as e:
        print(f"Missing key in experiment_dict: {e}")


def update_variable_priority(experiment_dict: dict[Any], experiment: str) -> dict[str]:
    """
    Update the variables for a single experiment with priority comments.

        :param experiment_dict: The dictionary containing all experiments and their associated variables.
        :param experiment: The experiment whose variables are being updated.
        :returns: A dictionary of variable name and priority level key-value pairs for a single experiment.
    """
    variable_dict = {}

    core_priority, high_priority, med_priority, low_priority = get_priority_labels(
        experiment_dict, experiment
    )

    # Convert required priorities to sets to improve performance.
    med_set = set(med_priority)
    low_set = set(low_priority)
    # Check all labels against their priority status and label accordingly.
    for variable in chain(core_priority, high_priority, med_priority, low_priority):
        if variable in med_set:
            priority = " # priority=medium"
        elif variable in low_set:
            priority = " # priority=low"
        else:
            priority = ""
        # Update dictionary with variable name as key and priority as value.
        variable_dict[variable] = priority

    return variable_dict


def match_variables_with_mappings(
    mappings_dict: list[dict[dict[str]]],
    experiment_dict: dict[Any],
    experiment: str,
    variable_dict: dict[str],
) -> dict[str]:
    """
    Verify the production status of each variable for each variable for a single experiment.

        :param mappings_dict: The dictionary containing mapping information for all variables.
        :param experiment_dict: The dictionary containing all experiments and their associated variables.
        :param experiment: The experiment whose variables are being updated.
        :param variable_dict: The dictionary of variable name and priority level key-value pairs for a single experiment.
        :returns: An updated dictionary containing production status for variables marked "do-not-produce".
        :raises KeyError: If labels list cannot be accessed from mapping_dict.
        :raises IndexError: If the title is unable to be split appropriately.
    """
    core_priority, high_priority, med_priority, low_priority = get_priority_labels(
        experiment_dict, experiment
    )
    # Convert all variables to sets to improve performance.
    priority_sets = set(chain(core_priority, high_priority, med_priority, low_priority))

    # Loop over all variables to find those labelled as "do-not-produce" and mark them as such.
    for map in mappings_dict:
        try:
            title = map.get("title", "")
            labels = map.get("labels", [])
            var = re.search(r"Variable\s+([^\s(]+)", title).group(1)
            # Overriding any existing "priority" value in the dict is acceptable since do-not-produce takes precedence.
            if var in priority_sets and "do-not-produce" in labels:
                variable_dict[var] = " # do-not-produce"
        except (KeyError, IndexError) as e:
            print(f"ERROR: Unable to obtain production label from mapping: {e}")

    return variable_dict


def reformat_varaible_names(
    variable_dict: dict[str], mappings_dict: list[dict[dict[str]]]
) -> dict[str]:
    """
    Reformats the name of each variable from realm.variable.branding.frequency.region to
    realm/variable_branding@frequency:stream for a single experiment.

        :param variable_dict: An updated dictionary containing production status for variables marked "do-not-produce".
        :param mappings_dict: The dictionary containing mapping information for all variables.
        :returns: An updated dictionary containing the reformatted variable names as keys and priority/production status
        as values.
    """
    renamed_variable_dict = {}
    variable_to_stream = {}

    # Access stash entries dictionary for each variable and check if it contains values.
    for map in mappings_dict:
        title = map.get("title", "")
        stream = ""
        var = re.search(r"Variable\s+([^\s(]+)", title).group(1)
        stash_entries = map.get("STASH entries", [])
        # If stash entries contains any values get the usage profile.
        if stash_entries:
            usage_profile = stash_entries[0].get("usage_profile", "")
            # Map usage profile to stream.
            stream = usage_profile.replace("UP", "ap") if usage_profile else ""
        # Create a local dictionary to pair variables and their streams.
        variable_to_stream[var] = stream

    # Reformat all original variable names to realm/variable_branding@frequency:stream (separate loop for performance).
    for key, value in variable_dict.items():
        parts = key.split(".")
        if len(parts) < 4:
            raise KeyError(f"{key} has unexpected format. Expected: realm.variable.branding.frequency.region")

        realm, variable, branding, frequency = parts[:4]
        stream = variable_to_stream.get(key, "")

        if stream:
            new_varaible_name = f"{realm}/{variable}_{branding}@{frequency}:{stream}"
        else:
            new_varaible_name = f"{realm}/{variable}_{branding}@{frequency}"

        # Update the original dictionary with the reformatted variable names.
        renamed_variable_dict[new_varaible_name] = value

    return renamed_variable_dict


def format_outfile_content(renamed_variable_dict: dict[str]) -> list[str]:
    """
    Reformats the key value pairs into single line plain text for a single experiment.

        :param renamed_variable_dict: An updated dictionary containing the reformatted variable names as keys and
        priority/production status as values.
        :returns: A list of lines to populate the plain text file with.
    """
    lines = []
    for key, value in renamed_variable_dict.items():
        if value:
            line = f"#{key}{value}\n"
        else:
            line = f"{key}{value}\n"
        lines.append(line)

    return lines


def generate_variable_lists() -> None:
    """
    Generates the variable list files for all experiments.
    """
    # Call required source files.
    experiments_filepath = Path("reference_information/dr-1.2.2.2_all.json")
    mappings_filepath = Path("reference_information/mappings.json")
    experiment_dict = open_source_jsons(experiments_filepath)
    mappings_dict = open_source_jsons(mappings_filepath)

    # Create output file path.
    outdir = Path(f"variables/{experiment_dict['Header']['dreq content version']}")
    os.makedirs(outdir, exist_ok=True)

    # Loop over all listed experiments.
    for experiment in tqdm(
        experiment_dict["experiment"],
        desc="Generating variable lists...",
        unit="file",
        dynamic_ncols=True,
    ):
        variable_dict = update_variable_priority(experiment_dict, experiment)
        variable_dict = match_variables_with_mappings(mappings_dict, experiment_dict, experiment, variable_dict)
        variable_dict = reformat_varaible_names(variable_dict, mappings_dict)

        # Save to plain text file.
        outfile = outdir / f"{experiment}.txt"
        with open(outfile, "w") as f:
            for line in format_outfile_content(variable_dict):
                f.write(line)

    print(f"SUCCESSFULLY GENERATED {len(experiment_dict['experiment'])} FILES")


if __name__ == "__main__":
    generate_variable_lists()
