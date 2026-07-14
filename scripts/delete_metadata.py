# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""This script is designed to delete workflow metadata configuration files and all other associated files.

Example command line usage:
`python scripts/delete_metadata.py <workflow_id>`
"""
import argparse
import os
import configparser
import sys

from pathlib import Path

from constants import DR_VERSION


def arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take source file paths from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.

    """
    parser = argparse.ArgumentParser(description="Delete a workflow metadata configuration file and all associated "
                                     "files.")
    parser.add_argument("workflow_id", help="The workflow ID associated with the workflow.")

    return parser.parse_args()


def get_variable_list_filename(filename: Path, workflow_id: str) -> str:
    """Returns the name of the corresponding variable list file associated with the given workflow ID.

    Parameters
    ----------
    filename: Path
        The path of the workflow metadata configuration file.
    workflow_id: str
        The workflow ID whose information is being deleted

    Returns
    -------
    str
        The corresponding variable list file associated with the given workflow ID.
    """
    config = configparser.ConfigParser()
    config.read(filename)

    return f"{workflow_id}_{config['metadata']['experiment_id']}_{config['metadata']['model_id']}.txt"


def main():
    """Main"""
    args = arg_parser()
    workflow_id = args.workflow_id

    # Confirm that the metadata file exists, we need information from this to identify the correct variable list.
    config_file_path = Path("workflow_metadata") / f"{workflow_id}.cfg"
    if not os.path.exists(config_file_path):
        print(f"Workflow metadata file for `{workflow_id}` does not exist.")
        sys.exit()

    # Identify the variable list path using information in the metadata config file
    variable_list_filename = get_variable_list_filename(config_file_path, workflow_id)
    variable_list_file_path = Path("variables") / f"v{DR_VERSION}" / variable_list_filename

    count = 0
    for file in [config_file_path, variable_list_file_path]:
        # Check each file exists before attempting to remove to avoid FileNotFound errors.
        if os.path.exists(file):
            os.remove(file)
            print(f"Successfully deleted {file}")
            count += 1
        else:
            print(f"File '{file}' does not exist. Skipping...")

    print(f"Removed {count} files for workflow {workflow_id}")


if __name__ == "__main__":
    main()
