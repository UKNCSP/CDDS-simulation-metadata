# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates a variable list the given experiment at the current data request version.

This script scans two source files containing CMIP experiments, their associated variables and the variable metadata
such as priority level and production labels. Each variable is labelled accordingly and commented out as necessary.
Each variable list is then saved to a plain text file.

THIS SCRIPT CURRENTLY CONSIDERS GLOBAL VARIABLES ONLY. NON-GLOBAL VARIABLES ARE FILTERED OUT WITHIN THE FUNCTION
reformat_variable_names().

This script can take inputs either directly from an issue body (as part of the github action `process_new_metadata.yml`
using '.github/ISSUE_TEMPLATE/add_workflow_metadata.yml') or through the command line for adhoc usage.

Note that this script is used as part of '.github/workflows/process_new_metadata.yml' and is the backbone of
'scripts/update-all_variable_lists.py' which is used in '.github/workflows/update_mappings.yml'. Changes to this script
may result in errors when running these corresponding files.

Example command line usage:
"python scripts/generate_variable_lists.py --workflow_id a-bc123 --experiment 1pctCO2 --model UKESM1-3
--variant_label r1i1p1f1"
"""

import argparse
import re
import os
from itertools import chain
from pathlib import Path

from common import read_json, get_issue, process_metadata
from constants import (REF_INFO_DIR, MAPPINGS_FILE_LOCATION, KNOWN_ISSUES_DICT_FILE_LOCATION, DR_FILE_LOCATION,
                       DR_VERSION)

ICEMOD_STREAMS = {
    "UKCM2": ["inm", "ind"],
    "HadGEM3-GC5": ["inm", "ind"]
}
FILE_HEADER = "# Note: only global variables are currently producible by CDDS\n"
BLANK_FILE_CONTENT = [FILE_HEADER,
                      "\n# This experiment is not currently defined in the data request.\n",
                      "# As a result, a variable list could not be generated automatically.\n",
                      "# The required variables for this experiment must be defined manually.\n"]


def set_arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take source file paths from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.

    """
    parser = argparse.ArgumentParser(description="Generate a variable list (global variables only) for a given list "
                                     "experiments using provided data request and mapping information.")
    parser.add_argument("--workflow_id", help="The workflow ID associated with this workflow.")
    parser.add_argument("--experiment", help="The experiment to generate a variable lists for.")
    parser.add_argument("--model", help="The model associated with the experiment that has been run.")
    parser.add_argument("--variant_label", help="The variant label associated with the experiment that has been run.")

    return parser.parse_args()


def collect_key_variables(args) -> tuple[str, str, str, str]:
    """Collects key variables (workflow_id, experiment and model). This can come directly from an
    issue body or the command line. If no command line arguments are given, the issue body is used. If neither are
    available, a RuntimeError is raised.

    Returns
    -------
    tuple(str, str, str, str, str)
        input_method, workflow_id, experiment, model and variant label.

    Raises
    ------
    RuntimeError
        If no command line arguments or issue body can be found.
    argparse.ArgumentError
        If some but not all arguments are given.
    """
    arguments = [args.workflow_id, args.experiment, args.model, args.variant_label]
    issue_body = get_issue()['body']
    if not any(arguments) and not issue_body:
        raise RuntimeError("No command line arguments or issue body provided.")

    if issue_body:
        # Note if an issue body is being used and get the required info
        print("No command line arguments given, using workflow_id, experiment and model given in the issue body.")
        match = re.findall(r"### (.+?)\n\s*\n?(.+)", issue_body)
        meta_dict = process_metadata(match)
        return ("issue", meta_dict["model_workflow_id"], meta_dict["experiment_id"], meta_dict["model_id"],
                meta_dict["variant_label"])

    elif args:
        inputs = ["--workflow_id", "--experiment", "--model", "--variant_label"]
        for input_flag, argument in zip(inputs, arguments):
            if not argument:
                raise argparse.ArgumentError(argument=argument, message=f"Missing argument: {input_flag}")
        return "args", args.workflow_id, args.experiment, args.model, args.variant_label


def get_grouped_priority_labels(experiment_dict: dict, experiment: str) -> dict:
    """Creates a dictionary of labels grouped by priority (core, high, med, low) for a single experiment using the
    current version of the data request.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.

    Returns
    -------
    dict
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
    experiment. This mainly ensures the .glb is always given in lower case.

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
        # Only apply a priority label if the priority is medium or low. High and core priority variables are left
        # without a priority comment.
        for variable in variables:
            priority_comments[variable] = ([f"priority={'medium' if level == 'med' else 'low'}"]
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
            return mapping


def check_alias_dictionary(model: str) -> str:
    """If the model variable status file cannot be directly found, an alias list is checked to account for the crossover
    in naming convention between models. This function ensures that the script does not fail incorrectly and that each
    model points to the correct variable status file. This is specifically put in place to handle cases where UKCM2 is
    still being referred to as HadGem3-GC5.

    Parameters
    ----------
    model: str
        The model associated with the experiment that has been run.

    Returns
    -------
    str
        The corrected model based off of the model alias dictionary.

    Raises
    ------
    RuntimeError
        If no corrected model alias can be found.
    """
    alias_dict = read_json(REF_INFO_DIR / "model_id_alias.json")
    for accepted_model, alias in alias_dict.items():
        if model in alias:
            return accepted_model

    return model


def update_status_from_model(model: str, variable_dict: dict) -> tuple[dict, str]:
    """Annotates each global variable with its production status (i.e. approved, embargoed or do not produce) given in
    the model status dictionaries produced by 'scripts/create_variable_status_dict.py'.

    Parameters
    ----------
    model: str
        The model associated with the experiment that has been run.
    variable_dict: dict
        A dictionary of variables and their comments created based on priority level.

    Returns
    -------
    tuple[dict, str]
        An updated dictionary of variables and their comments created based on priority level and production status.
        An updated model ID if the direct input is associated with an alias.
    """
    # Attempt to use the original model given
    model = check_alias_dictionary(model)
    status_dict_path = REF_INFO_DIR / f"{model}_variable_status.json"
    if not status_dict_path.exists():
        raise FileNotFoundError(f"Status dictionary for {model} does not exist at {status_dict_path}")

    # Apply status labels to each variable, a single variable can have multiple labels.
    model_status_dict = read_json(status_dict_path)
    for variable, comment in variable_dict.items():
        if variable in model_status_dict:
            variable_dict[variable].insert(0, f"{model_status_dict[variable]}")
        else:
            variable_dict[variable].insert(0, "no-mapping-found")

    return variable_dict, model


def get_stream_from_XIOS(mapping: dict, model: str) -> str:
    """If there are no streams listed from the stash, this function aims to access a stream/substream from the XIOS
    entries for a single variable within a model.

    Parameters
    ----------
    mapping: dict
        The mapping information for a single variable.
    model: str
        The model associated with the experiment that has been run.

    Returns
    str:
        The corresponding stream for the given variable within the given model. Returns "" if no stream can be found.
    """
    xios_dict = mapping.get("XIOS entries")
    full_stream_info = xios_dict.get(model, "")

    # Extract just the stream for the information given in the XIOS info.
    stream = full_stream_info.split("`")[0] if full_stream_info else ""
    # ind/inm streams in UKCM2 models must be overriden to use the /icemod sub stream.
    if model in ICEMOD_STREAMS:
        if any(base_stream in stream for base_stream in ICEMOD_STREAMS.get(model)):
            stream = f"{stream.split('/')[0]}/icemod"

    return stream


def get_streams(experiment_dict: dict, experiment: str, mappings_dict: list[dict], model: str) -> dict[str, str]:
    """Creates a dictionary for variables and their associated output stream for a single experiment.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.
    model: str
        The model ID.

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
        if not mapping:
            streams[variable] = ""
            continue

        stream = mapping.get("stream").lower()
        if "fx" in mapping.get("labels") and not stream:
            stream = apply_fx_streams(variable)
        # If theres no stream in STASH and the variable is not fixed, look for a stream in the XIOS info.
        if not stream:
            stream = get_stream_from_XIOS(mapping, model)

        streams[variable] = stream

    return streams


def apply_fx_streams(variable):
    realm = variable.split(".")[0]
    if realm in ["ocean", "ocnBgchem", "seaIce"]:
        return "ofx"
    elif realm in ["atmos", "aerosol", "atmosChem", "land", "landIce"]:
        return "afx"
    else:
        raise RuntimeError(f"Unable to apply stream to {variable}, unrecognsied realm `{realm}`")


def reformat_variable_names(
        experiment_dict: dict, experiment: str, mappings_dict: list[dict], variable_dict: dict, new_model: str
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
    new_model: str
        The updated model ID.

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
    streams = get_streams(experiment_dict, experiment, mappings_dict, new_model)

    # Reformat all original variable names to realm/variable_branding@frequency:stream.
    for variable, comment in variable_dict.items():
        parts = variable.split(".")
        if len(parts) < 5:
            raise KeyError(f"{variable} has unexpected format. Expected: realm.variable_id.branding.frequency.region")
        realm, variable_name, branding, frequency, region = parts[:5]
        stream = streams.get(variable, "")

        if frequency == "yr":
            comment.insert(0, "Yearly variables unable to be processed at this time")

        # Filter out any non global variables
        if region == "glb":
            new_variable_name = (f"{realm}/{variable_name}_{branding}@{frequency}:{stream}" if stream else
                                 f"{realm}/{variable_name}_{branding}@{frequency}")

            # Create new dictionary with the reformatted variable names to avoid key errors in the original dict.
            renamed_variable_dict[new_variable_name] = comment

    return renamed_variable_dict


def identify_known_issues(
        model: str, experiment: str, variant_label: str, renamed_variable_dict: dict[str, str]) -> dict[str, str]:
    """Identify all variables marked as "known issues" in a single experiment. This function is capable of flagging a
    variable as a known issue regardless of whether a stream is provided within the known issues dictionary or not.

    Parameters
    ----------
    model: str
        The model.
    experiment: str
        The experiment whose variables are being updated.
    variant_label: str
        The variant label.
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
    for variable in renamed_variable_dict:
        for source_id, experiment_id in known_issues_dict.items():
            if source_id == model:
                model_known_issues = known_issues_dict[source_id]
                variant_dicts = (model_known_issues.get(experiment), model_known_issues.get("*"))
                for variant_dict in variant_dicts:
                    if variant_dict:
                        for known_issues_variant, var_list in variant_dict.items():
                            if (known_issues_variant in ("*", variant_label) and variable.split(":")[0] in var_list and
                                "known-issue" not in renamed_variable_dict[variable]):
                                renamed_variable_dict[variable].insert(0, "known-issue")

    return renamed_variable_dict


def process_variable_dict(
        experiment_dict: dict, experiment: str, model: str, variant_label: str, mappings_dict: list[dict]
    ) -> tuple[dict, str]:
    """Processes the variable dictionary against all functions to get a complete dictionary of renamed variables and
    their associated status. This serves as a wrapper script for all variable list processing.

    Parameters
    ----------
    experiment_dict: dict
        The dictionary containing all experiments and their associated variables.
    experiment: str
        The experiment whose variables are being updated.
    model: str
        The model ID.
    variant_label: str
        The variant label.
    mappings_dict: list[dict]
        The dictionary containing mapping information for all variables.

    Returns
    -------
    tuple[dict, str]
        An updated dictionary containing the reformatted variable names and their associated status.
        The given model ID.
    """
    variable_dict = {}
    variable_dict = set_priority_comments(experiment_dict, experiment)
    variable_dict, new_model = update_status_from_model(model, variable_dict)
    variable_dict = reformat_variable_names(experiment_dict, experiment, mappings_dict, variable_dict, new_model)
    variable_dict = identify_known_issues(model, experiment, variant_label, variable_dict)

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
        # Comment out all variables apart from those marked as approved.
        if "approved" in comment and "known-issue" not in comment:
            lines.append(f"{variable}  # {', '.join(comment)}\n")
        elif comment:
            lines.append(f"#{variable}  # {', '.join(comment)}\n")
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
    if "do-not-produce (not available with this model)" in line:
        return 8
    elif "unknown (no stream information available)" in line:
        return 6
    elif "do-not-produce" in line:
        return 7
    elif "known-issue" in line:
        return 5
    elif "Yearly variables unable to be processed at this time" in line:
        return 4
    elif "embargoed" in line:
        return 3
    elif "priority=low" in line:
        return 2
    elif "priority=medium" in line:
        return 1

    return 0


def save_outfile(outfile: Path, renamed_variable_dict: dict[str, str]) -> None:
    """Saves a single file to a plain text format.

    Parameters
    ----------
    outfile: Path
        The output path.
    renamed_variable_dict: dict[str, str]
        An updated dictionary containing the reformatted variable names as keys and priority/production status as
        values.
    """
    lines = format_outfile_content(renamed_variable_dict)
    with open(outfile, "w") as f:
        f.write(FILE_HEADER)
        for line in sorted(lines, key=sort_key):
            f.write(line)


def generate_variable_lists() -> None:
    """
    Generates the variable list files for all experiments.
    """
    args = set_arg_parser()
    input_method, workflow_id, experiment, model, variant_label = collect_key_variables(args)
    experiment_dict = read_json(DR_FILE_LOCATION)
    mappings_dict = read_json(MAPPINGS_FILE_LOCATION)

    # Create output file path.
    outdir = Path(f"variables/v{DR_VERSION}")
    outfile = outdir / f"{workflow_id}_{experiment}_{model}.txt"
    os.makedirs(outdir, exist_ok=True)

    if not experiment_dict["experiment"].get(experiment, None):
        with open(outfile, "w") as f:
            f.writelines(BLANK_FILE_CONTENT)
    else:
        # Process and save the variable dictionary.
        variable_dict = process_variable_dict(experiment_dict, experiment, model, variant_label, mappings_dict)
        save_outfile(outfile, variable_dict)

    # Print the output filename the gh env if using inputs from an issue.
    if input_method == "issue":
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh:
            gh.write(f"filename={outfile}")

    print(f"Successfully generated variable list: {outfile}")


if __name__ == "__main__":
    generate_variable_lists()
