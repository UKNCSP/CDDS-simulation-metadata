# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script generates the variable status dictionaries for each model/source.
"""
from pathlib import Path
import json
from difflib import get_close_matches


def open_json(path: Path) -> dict:
    """Opens a single JSON file as a dictionary.

    Parameters
    ----------
    path: Path
        The path of the file to be opened.

    Returns
    -------
    dict
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


def save_json(model: str, dictionary: dict) -> None:
    """Saves a single dictionary to JSON format.

    Parameters
    ----------
    model: str
        The model associated with the dictionary that is being saved.
    dictionary: dict
        A dictionary of each variable in a model and its associated status.
    """
    filename = f"{model}_variable_status.json"
    outdir = Path("reference_information")
    outfile_path = outdir / filename
    with open(outfile_path, "w") as fh:
        json.dump(dictionary, fh, indent=4)


def _process_override(mappings_dict):
    model = input("Input the model for whos variables status you wish to override: ")
    all_models = get_all_models(mappings_dict)
    if model not in all_models:
        print(f"Model not regognised, did you mean {get_close_matches(model, all_models)[0]}?")
        _process_override(mappings_dict)
    status = input("What status would you like to assign all variables for this model? ")
    if status not in ["approved", "do-not-produce", "embargoed"]:
        print(f"Status not regognised, please choose from 'approved', 'do-not-produce' or 'embargoed'")
        _process_override(mappings_dict)

    confirmation = input(
        f"You have chosen to overide all variables in {model} with the status {status}, proceed? [Y/N] "
    )
    if confirmation not in ["Y", "N"]:
        print("Input not recognised")
        _process_override(mappings_dict)
    if confirmation == "Y":
        dictionary = open_json(Path(f"reference_information/{model}_variable_status.json"))
        for variable, value in dictionary.items():
            dictionary[variable] = status
        save_json(model, dictionary)
        repeat = input("Do you wish to override another model? ")
        if repeat not in ["Y", "y", "N", "n"]:
            print("Input not recognised, exiting script, your previous changes will not be affected...")
            pass
        if repeat in ["Y", "y"]:
            _optional_override(mappings_dict)
        else:
            pass
    elif confirmation == "N":
        _optional_override(mappings_dict)


def _optional_override(mappings_dict):
    override_request = input(
        "Is a status override required? Note this will affect every variable within the model [Y/N] "
    )
    if override_request not in ["Y", "N"]:
        print("Input not recognised")
        _optional_override(mappings_dict)
    if override_request == "Y":
        _process_override(mappings_dict)
    elif override_request == "N":
        pass


def generate_variable_status_dictionaries() -> None:
    """The main function responsible for generating the variable status dictionary for each model found in the
    mappings.json.
    """
    mappings_dict = open_json(Path("reference_information/mappings.json"))
    all_models = get_all_models(mappings_dict)
    for model in all_models:
        variable_status_dict = get_variable_status(mappings_dict, model)
        save_json(model, variable_status_dict)
        print(f"Processing variables for {model}..... Done")

    _optional_override(mappings_dict)


if __name__ == "__main__":
    generate_variable_status_dictionaries()
