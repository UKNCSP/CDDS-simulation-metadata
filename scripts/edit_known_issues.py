# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Command line tool to append or remove an item to/from the known issues dictionary used for CMIP7 variables.

Example command line usage: 'python scripts/edit_known_issues.py "UKESM1" "1pctCO2" "*" "atmos/tas_tavg-h2m-hxy-u@day"'.
"""

import argparse
from pathlib import Path
import json
import sys
from difflib import get_close_matches
import re

from common import read_json

MAPPING_FILE_LOCATION = Path("reference_information/mappings.json")
DR_FILE_LOCATION = Path("reference_information/dr-1.2.2.2_all.json")
KNOWN_ISSUES_DICT_FILE_LOCATION = Path("reference_information/known_issues.json")


def arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take user inputs from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.
    """
    parser = argparse.ArgumentParser(description=("This is a command line tool to append or remove an item from the "
                                                  "known_issues.json file."))

    parser.add_argument("source_id", help="The source id.")
    parser.add_argument("experiment_id", help=("The experiment id. To append to ALL experiment IDs, input '*' upon "
                                               "triggering the script."))
    parser.add_argument("variant_label", help=("The variant_label. To append to ALL variant labels, input '*' upon "
                                               "triggering the script."))
    parser.add_argument("variable", help="The variable.")

    return parser.parse_args()


def get_valid_source_ids() -> set:
    """Returns a set of all valid source IDs (also known as models) from the mappings file in reference information.

    Returns
    -------
    set
        A unique set of all valid source IDs.
    """
    valid_source_ids = set()
    mappings = read_json(MAPPING_FILE_LOCATION)
    for dictionary in mappings:
        valid_source_ids.add(dictionary["model"])

    return valid_source_ids


def get_valid_experiment_ids() -> list:
    """ Returns a list of all valid experiment IDs from the data request information file in reference information.

    Returns
    -------
    list
        A list of all valid experiment IDs.
    """
    data_req_info = read_json(DR_FILE_LOCATION)
    valid_experiment_ids = data_req_info["Header"]["Experiments included"]
    print(valid_experiment_ids)

    return valid_experiment_ids


def verify_user_input(args: argparse.Namespace) -> None:
    """Verifies the user input for source id, experiment id and variant label against a list of valid values or regular
    expression. If an exact match is not found then a closest match suggestion is given to the user.

    Parameters
    ----------
    args: argparse.Namespace
        The argument parser.

    Raises
    ------
    ValueError
        If an invalid entry is provided as an argument by the user.
    """
    user_inputs = [args.source_id, args.experiment_id]
    valid_inputs = [get_valid_source_ids(), get_valid_experiment_ids()]

    # Confirm that source id and experiment id are recognised and valid
    for user_input, valid_input_list in zip(user_inputs, valid_inputs):
        if user_input not in valid_input_list:
            guess = get_close_matches(user_input, valid_input_list)
            std_msg = f"'{user_input}' not recognised."
            msg = f"'{user_input}' not recognised, did you mean '{guess[0]}'?" if guess else std_msg
            raise ValueError(f"Invalid input value. {msg}")

    # Confirm that the variant label matches the expected regular expression
    regex_check = re.search(r"^(r\d+)(i\d+[a-e]{0,1})(p\d+)(f\d+)$", args.variant_label)
    if args.variant_label != "*" and regex_check is None:
        raise ValueError(f"Invalid input value. Variant label '{args.variant_label}' does not follow the expected "
                         "format.")


def get_add_or_delete_instructions() -> str:
    """Gets instructions from the user to determine if the entered item should be added to or removed from the known
    issues JSON.

    Returns
    -------
    str
        The command to either append or remove from the known issues JSON file.
    """
    instruction = input("Do you want to append or remove an entry from the known issues JSON? [append/remove] ")
    if instruction not in ["append", "remove"]:
        print("Input not recognised")
        get_add_or_delete_instructions()

    return instruction


def confirm_input_with_user(args: argparse.Namespace, instruction: str) -> None:
    """Requests written confirmation from the user that they want to append the given information to the JSON.

    Parameters
    ----------
    args: argparse.Namespace
        The argument parser.
    """
    information = (f"Variable: {args.variable}\nSource ID (Model ID): {args.source_id}\nExperiment ID: "
                   f"{args.experiment_id}\nVariant label: {args.variant_label}")
    print(f"\nYou are attempting to {instruction.upper()} the following information...\n{information}")

    response = input("Continue? [Y/N] ")
    if response == "N":
        ("Aborting...")
        sys.exit()

    # Recursively trigger the function if an invalid input is given by the user.
    if response not in ["Y", "N"]:
        print("Input not recognised")
        confirm_input_with_user(args, instruction)


def check_if_input_already_exists(source_dict: dict, args: argparse.Namespace) -> int:
    """Checks if the entry already exists and hence is a known issue. If the entry already exists the script returns an
    exit code 1 and 0 if it does not. This is used later to determine if the requested add or remove action is possible.

    Parameters
    ----------
    source_dict: dict
        The dictionary of known issues.
    args: argparse.Namespace
        The argument parser.

    Returns
    -------
    int:
        Returns 1 if the entry already exists and 0 if it does not.
    """
    if args.source_id in source_dict.keys():
        source_id_dict = source_dict[args.source_id]
        if args.experiment_id in source_id_dict.keys():
            exp_dict = source_id_dict[args.experiment_id]
            if args.variant_label in exp_dict.keys() and args.variable in exp_dict[args.variant_label]:
                return 1

    return 0


def append_to_issues_dict(source_dict: dict, args: argparse.Namespace) -> dict:
    """Adds the new entry to the issues dictionary.

    Parameters
    ----------
    source_dict: dict
        The dictionary of known issues.
    args: argparse.Namespace
        The argument parser.

    Returns
    -------
    dict
        The updated dictionary with the new entry.
    """
    if args.source_id not in source_dict.keys():
        source_dict[args.source_id] = {}
    if args.experiment_id not in source_dict[args.source_id].keys():
        source_dict[args.source_id][args.experiment_id] = {}
    if args.variant_label not in source_dict[args.source_id][args.experiment_id].keys():
        source_dict[args.source_id][args.experiment_id][args.variant_label] = []

    variable_list = source_dict[args.source_id][args.experiment_id][args.variant_label]
    variable_list.append(args.variable)

    return source_dict


def remove_from_issues_dict(source_dict: dict, args: argparse.Namespace) -> dict:
    """Deletes the input entry from the known issues JSON.

    Parameters
    ----------
    source_dict: dict
        The dictionary of known issues.
    args: argparse.Namespace
        The argument parser.

    Returns
    -------
    dict
        The updated dictionary after removing the entry.
    """
    source_dict[args.source_id][args.experiment_id][args.variant_label].remove(args.variable)

    return source_dict


def main():
    """Holds the main body of the script"""
    args = arg_parser()
    source_dict = read_json(KNOWN_ISSUES_DICT_FILE_LOCATION)
    instruction = get_add_or_delete_instructions()
    verify_user_input(args)
    confirm_input_with_user(args, instruction)
    existance = check_if_input_already_exists(source_dict, args)

    if instruction == "append":
        if existance == 0:
            updated_dict = append_to_issues_dict(source_dict, args)
            print("\nEntry successfully added")
        elif existance == 1:
            print("\nThis entry does not exist and hence cannot be deleted.")
            sys.exit()

    elif instruction == "remove":
        if existance == 1:
            updated_dict = remove_from_issues_dict(source_dict, args)
            print("\nEntry successfully deleted")
        elif existance == 0:
            print("\nThis entry does not exist and hence cannot be deleted.")
            sys.exit()

    with open(Path("reference_information/known_issues.json"), "w") as outfile:
        json.dump(updated_dict, outfile, indent=4)


if __name__ == "__main__":
    main()
