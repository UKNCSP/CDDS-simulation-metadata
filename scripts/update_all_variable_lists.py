# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Update all variables lists using existing workflow metadata."""

import os
import configparser

from pathlib import Path

from common import read_json
from constants import DR_FILE_LOCATION, MAPPINGS_FILE_LOCATION
from generate_variable_lists import process_variable_dict, save_outfile

WORKFLOW_METADATA_FILE_LOCATION = Path("workflow_metadata")


def get_all_workflow_metadata() -> list:
    """Returns a list of the paths of all workflow metadata configuration files within the repository.

    Returns
    -------
    list
        A list of all workflow metadata configuration files.
    """
    return list(WORKFLOW_METADATA_FILE_LOCATION.glob('*.cfg'))


def extract_key_workflow_information(filename: Path) -> dict:
    """Returns a dictionary of the key information required from a single configuration file e.g. the experiment id,
    model id and workflow id.

    Parameters
    ----------
    filename: Path
        The path of the configuration file.

    Returns
    -------
    dict
        A dictionary fo the key information required from the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(filename)

    return {
        "experiment_id": config["metadata"]["experiment_id"],
        "model_id": config["metadata"]["model_id"],
        "workflow_id": config["data"]["model_workflow_id"]
    }


def main():
    """Holds the main body of the script"""
    experiment_dict = read_json(DR_FILE_LOCATION)
    mappings_dict = read_json(MAPPINGS_FILE_LOCATION)

    # Create output file path.
    outdir = Path(f"variables/{experiment_dict['Header']['dreq content version']}")
    os.makedirs(outdir, exist_ok=True)

    all_workflow_metadata = get_all_workflow_metadata()
    num_successful_files = 0
    num_failed_files = 0

    for filename in all_workflow_metadata:
        try:
            key_info = extract_key_workflow_information(filename)
            variable_dict, model = process_variable_dict(experiment_dict, key_info["experiment_id"],
                                                         key_info["model_id"], mappings_dict)
            save_outfile(outdir, key_info["workflow_id"], key_info["experiment_id"], model, variable_dict)
            num_successful_files += 1
        except Exception as e:
            print(f"WARNING: Unable to generate updated variable list for {key_info["workflow_id"]}. \n{e}")
            num_failed_files += 1

    success_msg = f"\n SUCCESSFULLY REGENERATED {num_successful_files}/{num_successful_files + num_failed_files} FILES"
    failure_msg = f"\nWARNING: {num_failed_files} files failed."
    print("\n", "=" * 50, success_msg) if num_failed_files == 0 else print("\n", "=" * 50, success_msg, failure_msg)


if __name__ == "__main__":
    main()
