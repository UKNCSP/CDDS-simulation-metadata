# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.

"""
This script scans all workflow metadata files and validates their structure and contents.
"""

import configparser
import glob
import re
import sys
from pathlib import Path

from constants import (
    DATA,
    DATETIME_FIELDS,
    METADATA,
    MISC,
    PARENT_REQUIRED,
    REGEX_FORMAT,
    REQUIRED,
    SECTIONS,
)


def get_metadata_files() -> list[str]:
    """
    Creates a list of all existing cfg files to be checked.

    :returns: List of cfg files to be checked.
    """
    glob_string = Path("workflow_metadata/*.cfg")
    cfg_files = glob.glob(str(glob_string))

    return cfg_files


def validate_structure(config: configparser, failures: bool) -> bool:
    """
    Validates the structure of a single .cfg file.

    :param config: The config parser.
    :param failures: The status of the file validation (True/False).
    :returns: The status of the file validation.
    """
    missing_sections = []
    unexpected_sections = []
    missing_keys = []
    unexpected_keys = []
    sections_in_config = set(config.sections())
    SECTION_DICT = {
        "metadata": METADATA,
        "data": DATA,
        "misc": MISC
    }

    # Verify the correct sections are present in the correct order
    if not sections_in_config == SECTIONS:
        print("--> WARNING: File does not contain the required sections.")
        unexpected_sections = sections_in_config - SECTIONS
        missing_sections = SECTIONS - sections_in_config

        if unexpected_sections:
            print(f"    --> UNEXPECTED SECTIONS: [{', '.join(unexpected_sections)}]")
        if missing_sections:
            print(f"    --> MISSING SECTIONS: [{', '.join(missing_sections)}]")
        failures = True

    # Verify the correct keys are in the correct section
    for section in SECTIONS:
        keys = set(config[section].keys()) if section in config else set()
        target = set(SECTION_DICT[section])

        missing_keys = target - keys
        if section not in missing_sections:
            unexpected_keys = keys - target
        if missing_keys or unexpected_keys:
            print(f"--> WARNING: [{section}] does not contain the required keys.")
            if missing_keys:
                print(f"    --> MISSING KEYS: {missing_keys}")
            if unexpected_keys:
                print(f"    --> UNEXPECTED KEYS: {unexpected_keys}")
            failures = True

    return failures


def validate_required_fields(config: configparser, failures: bool) -> bool:
    """
    Validates the contents of the required fields for a single .cfg file.

    :param config: The config parser.
    :param failures: The status of the file validation (True/False).
    :returns: The status of the file validation.
    """
    # Verify that all required fields are not None
    for section in config.sections():
        section_data = config[section]
        for key, value in section_data.items():
            if key in REQUIRED and not value:
                print(f"--> WARNING: {key} is a required field and cannot be empty.")
                failures = True

            if key == "branch_method":
                if value == "standard":
                    for parent_key in PARENT_REQUIRED:
                        if section_data.get(parent_key) in (None, ""):
                            print(f"--> WARNING: {parent_key} is a required field and cannot be empty.")
                            failures = True
                elif value == "no parent":
                    for parent_key in PARENT_REQUIRED:
                        if section_data.get(parent_key) not in (None, ""):
                            print(f"--> WARNING: {parent_key} is not required when using 'no parent' branch method.")
                            failures = True

            if key == "mass_data_class":
                if value == "ens" and not section_data.get("mass_ensemble_member"):
                    print("--> WARNING: mass_ensemble_member is a required field and cannot be empty.")
                    failures = True
                if value == "crum" and section_data.get("mass_ensemble_member"):
                    print("--> WARNING: mass_ensemble_member is not needed when using 'crum' mass data class.")
                    failures = True

    return failures


def validate_field_inputs(config: configparser, failures: bool, REGEX_DICT: dict[str]) -> bool:
    """
    Validates the inputs of a single .cfg file.

    :param config: The config parser.
    :param failures: The status of the file validation (True/False).
    :returns: The status of the file validation.
    """
    for section in config.sections():
        for key, value in config[section].items():
            # Verify datetime inputs
            if key == "branch_method" and value == "standard":
                DATETIME_FIELDS.add("branch_date_in_child")
                DATETIME_FIELDS.add("branch_date_in_parent")
            if key in DATETIME_FIELDS:
                if not REGEX_DICT["datetime_pattern"].fullmatch(value):
                    print(f"--> WARNING: {key} is an invalid datetime format.")
                    failures = True

            # Verify workflow model ID structure
            if key == "model_workflow_id":
                if not REGEX_DICT["workflow_pattern"].fullmatch(value):
                    print(f"--> WARNING: {key} is incorrectly formatted.")
                    failures = True

            # Verify variant label structure
            if key == "variant_label":
                if not REGEX_DICT["variant_pattern"].fullmatch(value):
                    print(f"--> WARNING: {key} is incorrectly formatted.")
                    failures = True

            # Verify that atmospheric timestep is an integer
            if key == "atmos_timestep":
                if not value.isdigit() or int(value) < 0:
                    print(f"--> WARNING: {key} is invalid.")
                    failures = True

            # Verify that no fields have the value "_No response_"
            if value == "_No response_":
                print(f"--> WARNING: {key} contains invalid entry ('_No response_').")
                failures = True

    return failures


def print_results_to_user(cfg_files: list[str], failed_files: list[str]) -> None:
    """
    Prints validation information for all files back to the user.

    :param cfg_files: The complete list of files that were validated.
    :param failed_files: The list of files that failed validation.
    """
    print("\n==================================")
    print(
        f"SUCCESSFULLY VALIDATED: {len(cfg_files) - len(failed_files)}/{len(cfg_files)}"
    )
    print("==================================")
    if failed_files:
        print("\n==================================")
        print(f"{len(failed_files)} FAILED:")
        for file in failed_files:
            print(f"- {file}")
        print("==================================")
        sys.exit(1)


def main() -> None:
    """
    Holds the main body of the script.
    """
    failed_files = []
    REGEX_DICT = {
        "datetime_pattern": re.compile(REGEX_FORMAT["datetime"]),
        "workflow_pattern": re.compile(REGEX_FORMAT["model_workflow_id"]),
        "variant_pattern": re.compile(REGEX_FORMAT["variant_label"])
    }

    config = configparser.ConfigParser()
    cfg_files = get_metadata_files()

    for file in cfg_files:
        # Set default value for success
        failures = False

        # Perform validation
        config.read(file)
        print(f"\nChecking {str(Path(file).stem)}.cfg")
        validators = [validate_structure(config, failures),
                      validate_required_fields(config, failures),
                      validate_field_inputs(config, failures, REGEX_DICT)]
        for v in validators:
            failures += v

        # Create list of failed files
        if failures:
            failed_files.append(file)
        else:
            print("SUCCESS...")

    print_results_to_user(cfg_files, failed_files)


if __name__ == "__main__":
    main()
