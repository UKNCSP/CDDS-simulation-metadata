# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""This script generates the variable status dictionaries for each model/source ID.

This script is intended for command line usage in which the user will be given the option to manually override an entire
model variables status file with a given status. e.g. override all variables in UKESM1 with the status "embargoed". The
accepted status' are "approved", "do-not-produce" and "embargoed".

In the absence of a manual override, the variable status' are drawn from the mappings JSON and labelled appropriately.
"""

import json

from common import read_json
from constants import REF_INFO_DIR, MAPPINGS_FILE_LOCATION


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
        stash_model_list = mapping["models_in_stash"]
        xios_model_list = list(mapping["XIOS entries"].keys())
        model_list = stash_model_list + xios_model_list
        for model in model_list:
            models.add(model)

    return models


def get_variable_status(mappings_dict: list[dict], model: str) -> dict:
    """Gets the status of each variable for a single model.

    Parameters
    ----------
    mappings_dict: list[dict]
        The dictionary containing the mapping and model information for all variables.
    model: str
        The model.

    Returns
    -------
    dict
        A dictionary of each variable in a model and its associated status.
    """
    variable_status_dict = {}
    for mapping in mappings_dict:
        variable = mapping["branded_variable"]
        if (
            not mapping["models_in_stash"]
            and not mapping["XIOS entries"]
            and not any(label in mapping["labels"] for label in ('do-not-produce', 'fx'))
        ):
            variable_status_dict[variable] = "unknown (no stream information available)"
        elif model in mapping["models_in_stash"] or model in mapping["XIOS entries"].keys() or "fx" in mapping["labels"]:
            labels = mapping["labels"]
            if "do-not-produce" in labels:
                variable_status_dict[variable] = "do-not-produce"
            elif "diagnostic_review_ok" in labels:
                variable_status_dict[variable] = "approved"
            else:
                variable_status_dict[variable] = "embargoed"
        else:
            variable_status_dict[variable] = "do-not-produce (not available with this model)"

    return variable_status_dict


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
        json.dump(dict(sorted(dictionary.items(), key=lambda x: x[0])), fh, indent=4)


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


if __name__ == "__main__":
    generate_variable_status_dictionaries()
