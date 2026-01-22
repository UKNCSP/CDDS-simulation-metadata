# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the variable status dictionaries for each model/source.
"""
from pathlib import Path
import json
from difflib import get_close_matches
import sys

from scripts.common import read_json

REF_INFO_DIR = Path("reference_information")
MAPPINGS_FILE_LOCATION = REF_INFO_DIR / "mappings.json"


def get_all_models(mappings_dict: list[dict]) -> set:
    """Gets a list of all models.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.

    Returns
    -------
    set
        A unique set of all models that exist in the mappings dictionary.
    """
    models = set()
    for mapping in mappings_dict:
        models.add(mapping["model"])

    return models


def get_variable_status(mappings_dict: list[dict], model: str) -> dict:
    """Gets the status of each variable for a single model.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.
    model: str
        The model.

    Return
    ------
    dict
        A dictionary of each variable in a model and its associated status.
    """
    variable_status_dict = {}
    for mapping in mappings_dict:
        if mapping["model"] == model:
            if "approved" in mapping["labels"]:
                variable_status_dict[(mapping["branded_variable"])] = "approved"
            elif "do-not-produce" in mapping["labels"]:
                variable_status_dict[(mapping["branded_variable"])] = "do-not-produce"
            else:
                variable_status_dict[(mapping["branded_variable"])] = "embargoed"

    return variable_status_dict


def get_model_to_override(mappings_dict: list[dict]) -> str:
    """Returns the model whos variable status dictionary the user wishes to override.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.

    Returns
    -------
    model: str
        The model to override.
    """
    model = input("Input the model for whos variables you wish to override: ")
    all_models = get_all_models(mappings_dict)
    if model not in all_models:
        print(f"Model not regognised, did you mean {get_close_matches(model, all_models)[0]}?")
        get_model_to_override(mappings_dict)

    return model


def get_overriding_status() -> str:
    """Returns the status that the variables in the chosen model status dictionary will be overridden with.

    Returns
    -------
    status: str
        The new status of the variables. Can be "approved", "do-not-produce" or "embargoed".
    """
    status = input(f"What status would you like to assign all of the variables with? ")
    if status not in ["approved", "do-not-produce", "embargoed"]:
        print(f"Status '{status}' not regognised, please choose from 'approved', 'do-not-produce' or 'embargoed'")
        get_overriding_status()

    return status


def save_json(model: str, dictionary: dict) -> None:
    """Saves a single dictionary to JSON format.

    Parameters
    ----------
    model: str
        The model associated with the dictionary that is being saved.
    dictionary: dict
        A dictionary of each variable in a model and its associated status.
    """
    outfile_path = REF_INFO_DIR / f"{model}_variable_status.json"
    with open(outfile_path, "w") as fh:
        json.dump(dictionary, fh, indent=4)


def get_repeat_override_request(mappings_dict: list[dict]) -> None:
    """Determines if the user would like to override another model variable status dictionary file.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.
    """
    repeat = input("Do you wish to override another model? ")
    if repeat not in ["Y", "y", "N", "n"]:
        print("Input not recognised, exiting script, your previous changes will not be affected...")
        sys.exit()
    elif repeat in ["Y", "y"]:
        process_override(mappings_dict)
    else:
        sys.exit()


def request_override(mappings_dict: list[dict]) -> None:
    """Determines if the user would like to override model variable status dictionary file.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.
    """
    override_request = input(
        "Is a status override required? Note this will affect every variable within the model [Y/N] "
    )
    if override_request not in ["Y", "N"]:
        print("Input not recognised")
        request_override(mappings_dict)
    if override_request == "Y":
        process_override(mappings_dict)
    elif override_request == "N":
        sys.exit()


def process_override(mappings_dict) -> None:
    """Processes the override if requested. The requested override information is printed back to the user for
    confirmation and, upon approval, the requested file is adjusted as requested. This override affects every variables
    within the chosen model variable status file. The option is given to the user to override any number of the model
    files one at a time.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.
    """
    model = get_model_to_override(mappings_dict)
    status = get_overriding_status()

    confirmation = input(f"Overide all variables in {model} as {status}, proceed? [Y/N] ")
    if confirmation not in ["Y", "y", "N", "n"]:
        print("Input not recognised")
        process_override(mappings_dict)

    if confirmation == "Y":
        dictionary = read_json(REF_INFO_DIR / f"{model}_variable_status.json")
        for variable, value in dictionary.items():
            dictionary[variable] = status
        save_json(model, dictionary)
        get_repeat_override_request(mappings_dict)
    elif confirmation == "N":
        request_override(mappings_dict)


def generate_variable_status_dictionaries() -> None:
    """The main function responsible for generating the variable status dictionary for each model found in the
    mappings.json.
    """
    mappings_dict = read_json(MAPPINGS_FILE_LOCATION)
    all_models = get_all_models(mappings_dict)
    for model in all_models:
        variable_status_dict = get_variable_status(mappings_dict, model)
        save_json(model, variable_status_dict)
        print(f"Processing variables for {model}..... Done")

    request_override(mappings_dict)


if __name__ == "__main__":
    generate_variable_status_dictionaries()
