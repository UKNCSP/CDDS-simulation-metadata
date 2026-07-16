# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""This script generates the variable status dictionaries for each model/source ID.  Variable status' are drawn from the
mappings JSON and labelled appropriately.

This script is intended for command line usage but is incorporated as part of '.github/workflows/update_mappings.yml'.
Changes to this script may result in errors within this workflow.
"""

import json

from common import read_json
from constants import REF_INFO_DIR, MAPPINGS_FILE_LOCATION


def get_all_models(mappings_dict: list[dict]) -> set:
    """Gets a set of all models present in the mappings.json.

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
        # Check for models in both the STASH and XIOS, each variable should have entried in one of these tables.
        stash_model_list = mapping["models_in_stash"]
        xios_model_list = list(mapping["XIOS entries"].keys())
        model_list = stash_model_list + xios_model_list
        for model in model_list:
            models.add(model)

    return models


def get_variable_status(mappings_dict: list[dict], model: str) -> dict:
    """Returns a dictionary of each variable and its status for the given model. The status can be one of:

    - "approved" meaning that the variable has been produced and has passed the diagnostic review process successfully.
    - "do-not-produce" meaning that the variable has been marked as do-not-produce in the mappings hence cannot be
    produced, irrespective of the model used.
    - "do-not-produce (not available with this model)" meaning that the variable has no mapping information for the
    given model, hence it cannot be produced using this model.
    - "embargoed" meaning that the variable is technically producible with this model but has NOT yet passed the
    diagnostic review process successfully.
    - "unknown (no stream information available)" meaning that the variable exists in the mappings.json but there is no
    content in the stash or XIOS table and hence no stream information to use in processing. We have no way of knowing
    if this variable can be produced by this model.

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
    approved_labels = ["diagnostic_review_ok", "diagnostic_review_ok_OI_UKCM", "diagnostic_review_ok_OI_UKESM"]

    for mapping in mappings_dict:
        variable = mapping["branded_variable"]
        # Variables marked 'do-not-produce' and 'fx' are handled separately and unlikely to have any meaningfull
        # stream information. These require a more specific label.
        if (
            not mapping["models_in_stash"]
            and not mapping["XIOS entries"]
            and not any(label in mapping["labels"] for label in ('do-not-produce', 'fx'))
        ):
            variable_status_dict[variable] = "unknown (no stream information available)"

        elif (
            model in mapping["models_in_stash"]
            or model in mapping["XIOS entries"].keys()
            or "fx" in mapping["labels"]
        ):
            labels = mapping["labels"]
            if "do-not-produce" in labels:
                variable_status_dict[variable] = "do-not-produce"
            elif [item for item in approved_labels if item in labels]:
                variable_status_dict[variable] = "approved"
            # If all of the required information exists and a variable is not yet approved or marked as do-not-produce,
            # it must be marked as embargoed
            else:
                variable_status_dict[variable] = "embargoed"

        # Flag variables with no mention of the given model in their mapping inforamtion.
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
        print(f"Processing variables for {model}..... Done")  # Printed to terminal or actions logs for debugging


if __name__ == "__main__":
    generate_variable_status_dictionaries()
