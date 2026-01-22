# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the variable lists for each CMIP experiment for each data request version.

This script scans two source files containing CMIP experiments, their associated variables and the variable metadata
such as priority level and production labels. Each variable is labelled accordingly and commented out as necessary.
Each variable list is then saved to a plain text file containing the variables for that experiment.

THIS SCRIPT CURRENTLY CONSIDERS GLOBAL VARIABLES ONLY. NON-GLOBAL VARIABLES ARE FILTERED OUT WITHIN THE FUNCTION
reformat_variable_names().

Example command line usage:
"python scripts/generate_variable_lists.py 1pctCO2 UKESM1-3"
"""

import argparse
import os
from itertools import chain
from pathlib import Path

from scripts.common import read_json
from scripts.constants import REF_INFO_DIR, MAPPINGS_FILE_LOCATION, KNOWN_ISSUES_DICT_FILE_LOCATION, DR_FILE_LOCATION


def set_arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take source file paths from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.

    """
    parser = argparse.ArgumentParser(description="Generate a variable list (global variables only) for a given list "
                                     "experiments using provided data request and mapping information.")

    parser.add_argument("experiment", help="The experiment to generate a variable lists for.")
    parser.add_argument("model", help="The model associated with the experiment that has been run.")

    return parser.parse_args()


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
        "core": experiment_data.get("Core", []),
        "high": experiment_data.get("High", []),
        "med": experiment_data.get("Medium", []),
        "low": experiment_data.get("Low", []),
    }


def standardise_grouped_priority_labels(experiment_dict: dict, experiment: str) -> dict:
    """Creates a standardised dictionary of variable names grouped by priority (core, high, med, low) for a single
    experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    dict
        A dictionary of standardised variable names grouped by priority (core, high, med, low).
    """
    unstandardised_groups = get_grouped_priority_labels(experiment_dict, experiment)
    standardised_groups = {}
    for group, variable_list in unstandardised_groups.items():
        standardised_variable_list = []
        for variable in variable_list:
            standardised_variable_list.append(variable.replace(".GLB", ".glb"))
        standardised_groups[group] = standardised_variable_list

    return standardised_groups


def set_priority_comments(experiment_dict: dict, experiment: str) -> dict:
    """Sets the comment to be appended to each variable based off of their priority level for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    dict
        A dictionary of variables and their comments created based on priority level.
    """
    priority_comments = {}
    priority_dict = standardise_grouped_priority_labels(experiment_dict, experiment)
    for level, variables in priority_dict.items():
        for variable in variables:
            priority_comments[variable] = ([f" # priority={'medium' if level == 'med' else 'low'}"]
                                           if level in ("med", "low") else [])

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
    priority_dict = standardise_grouped_priority_labels(experiment_dict, experiment)

    return chain(priority_dict["core"], priority_dict["high"], priority_dict["med"], priority_dict["low"])


def get_mapping(mappings_dict: list[dict], variable: str) -> dict:
    """Identifies the correct dictionary within the mappings.json to read from.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.
    variable: str
        The variable whose mapping information is required.

    Returns
    -------
    dict
        The mapping information for a single variable.
    """
    for mapping in mappings_dict:
        if variable == mapping["branded_variable"]:
            mapping = mapping
            break

    return mapping


def update_status_from_model(model: str, variable_dict: dict) -> dict:
    """Annotates each global variable with its production status (i.e. approved, embargoed or do not produce).

    Parameters
    ----------
    model: str
        The model associated with the experiment that has been run.
    variable_dict: dict
        A dictionary of variables and their comments created based on priority level.

    Returns
    -------
    dict
        An updated dictionary of variables and their comments created based on priority level and production status.
    """
    model_status_dict = read_json(REF_INFO_DIR / f"{model}_variable_status.json")
    for variable, comment in variable_dict.items():
        if variable in list(model_status_dict.keys()):
            variable_dict[variable].insert(0, f" # {model_status_dict[variable]}")
        else:
            variable_dict[variable].insert(0, " # no-mapping-found")

    return variable_dict


def get_streams(experiment_dict: dict, experiment: str, mappings_dict: list[dict]) -> dict[str, str]:
    """Creates a dictionary for variables and their associated output stream for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.

    Returns
    -------
    dict[str, str]
        A dictionary containing variables and their associated output stream.
    """
    streams = {}

    # Access stash entries for each variable and check if it contains values.
    all_labels = get_all_variables(experiment_dict, experiment)
    for variable in all_labels:
        mapping = get_mapping(mappings_dict, variable)
        streams[variable] = mapping.get("stream")

    return streams


def reformat_variable_names(
    experiment_dict: dict, experiment: str, mappings_dict: list[dict], variable_dict: dict
) -> dict[str, str]:
    """Reformats the name of each variable from realm.variable.branding.frequency.region to
    realm/variable_branding@frequency:stream for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
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
    streams = get_streams(experiment_dict, experiment, mappings_dict)

    # Reformat all original variable names to realm/variable_branding@frequency:stream.
    for variable, comment in variable_dict.items():
        parts = variable.split(".")
        if len(parts) < 5:
            raise KeyError(f"{variable} has unexpected format. Expected: realm.variable.branding.frequency.region")

        realm, variable_name, branding, frequency, region = parts[:5]
        stream = streams.get(variable, "")

        # Filter out any non global variables
        if region == "glb":
            new_variable_name = (f"{realm}/{variable_name}_{branding}@{frequency}:{stream}" if stream else
                                 f"{realm}/{variable_name}_{branding}@{frequency}")

            # Create new dictionary with the reformatted variable names to avoid key errors in the original dict.
            renamed_variable_dict[new_variable_name] = comment

    return renamed_variable_dict


def identify_known_issues(experiment: str, renamed_variable_dict: dict[str, str]) -> dict[str, str]:
    """Identify all variables marked as "known issues" in a single experiment. This function is capable of flagging a
    variable as a known issue regardless of whether a stream is provided within the known issues dictionary or not.

    Parameters
    ----------
    experiment: str
        The experiment whose variables are being updated.
    renamed_variable_dict: dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production status as
        values.

    Returns
    -------
    dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production/issue status as
        values.
    """
    known_issues_dict = read_json(KNOWN_ISSUES_DICT_FILE_LOCATION)
    for variable in renamed_variable_dict.keys():
        for source_id, experiment_id in known_issues_dict.items():
            if any(value in list(known_issues_dict[source_id].keys()) for value in (experiment, "*")):
                try:
                    variant_dict = known_issues_dict[source_id][experiment]
                except KeyError:
                    variant_dict = known_issues_dict[source_id]["*"]
                for variant_label, variable_list in variant_dict.items():
                    if any(value in variable_list for value in (variable, variable.split(":")[0])):
                        renamed_variable_dict[variable] = " # known-issue"

    return renamed_variable_dict


def process_variable_dict(experiment_dict: dict, experiment: str, model: str, mappings_dict: list[dict]) -> dict:
    """Processes the variable dictionary against all functions to get a complete dictionary of renamed variables and
    their associated status.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.

    Returns
    -------
    dict
        An updated dictionary containing the reformatted variable names and their associated status.
    """
    variable_dict = {}
    variable_dict = set_priority_comments(experiment_dict, experiment)
    variable_dict = update_status_from_model(model, variable_dict)
    variable_dict = reformat_variable_names(experiment_dict, experiment, mappings_dict, variable_dict)
    variable_dict = identify_known_issues(experiment, variable_dict)

    return variable_dict


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

    Raises
    ------
    RuntimeError
        If a variable has no comment.
    """
    lines = []
    for variable, comment in renamed_variable_dict.items():
        if comment == " # approved":
            lines.append(f"{variable}{' '.join(comment)}\n")
        elif comment:
            lines.append(f"#{variable}{' '.join(comment)}\n")
        elif not comment:
            raise RuntimeError(f"An unrecognised variable '{variable}' with no model variable status was discovered "
                               "during processing. This likely means that a variable cannot be produced within the "
                               "given model but has bypassed the filtering process.")

    return lines


def sort_key(line: str) -> int:
    """The custom sort function passed to the sorted() function to define the variable order for a single experiment.

    Parameters
    ----------
    line: str
        A single line containing a single variable name and associated comments.

    Returns
    -------
    int
        The order of each label based on priority, variables with no specified priority will be assigned order 0 so that
        they appear at the top of the variable list.
    """
    if "do-not-produce" in line:
        return 5
    elif "no-mapping-found" in line:
        return 4
    elif "embargoed" in line:
        return 3
    elif "priority=low" in line:
        return 2
    elif "priority=medium" in line:
        return 1

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
    experiment_dict = read_json(DR_FILE_LOCATION)
    mappings_dict = read_json(MAPPINGS_FILE_LOCATION)

    # Create output file path.
    outdir = Path(f"variables_glb/{experiment_dict['Header']['dreq content version']}")
    os.makedirs(outdir, exist_ok=True)

    # Process and save the variable dictionary.
    variable_dict = process_variable_dict(experiment_dict, args.experiment, args. model, mappings_dict)
    save_outfile(outdir, args.experiment, variable_dict)

    print(f"SUCCESSFULLY GENERATED VARIABLE LIST FOR {args.experiment}")


if __name__ == "__main__":
    generate_variable_lists()
