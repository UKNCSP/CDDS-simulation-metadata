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


def validate_structure(config: configparser, file: str, failures: int) -> int:
    """
    Validates the structure of a single .cfg file.

        :param config: The config parser.
        :param file: The cfg file to be checked.
        :param failures: The number of files that have failed validations.
        :returns: The number of files that have failed validations.
    """
    # Verify the correct sections are present in the correct order
    missing_sections = []
    unexpected_sections = []
    if not config.sections() == SECTIONS:
        print(
            f"--> WARNING: {str(Path(file).stem)}.cfg does not contain the required sections."
        )
        unexpected_sections = [s for s in config.sections() if s not in SECTIONS]
        missing_sections = [s for s in SECTIONS if s not in config.sections()]
        if unexpected_sections:
            print(f"    --> UNEXPECTED SECTIONS: [{', '.join(unexpected_sections)}]")
        if missing_sections:
            print(f"    --> MISSING SECTION: [{', '.join(missing_sections)}]")
        failures += 1

    # Verify the correct keys are in the correct section
    missing_keys = []
    unexpected_keys = []
    for section in SECTIONS:
        try:
            keys = list(config[section].keys())
        except KeyError:
            pass

        if section == "metadata":
            target = METADATA
        elif section == "data":
            target = DATA
        elif section == "misc":
            target = MISC

        missing_keys = [k for k in target if k not in keys]
        if section not in missing_sections:
            unexpected_keys = [k for k in keys if k not in target]
        if missing_keys or unexpected_keys:
            print(f"--> WARNING: [{section}] does not contain the required keys.")
            if missing_keys:
                print(f"    --> MISSING KEYS: {', '.join(missing_keys)}")
            if unexpected_keys:
                print(f"    --> UNEXPECTED KEYS: {', '.join(unexpected_keys)}")
            failures += 1

    return failures


def Validate_required_fields(config: configparser, failures: int) -> int:
    """
    Validates the contents of the required fields for a single .cfg file.

        :param config: The config parser.
        :param failures: The number of files that have failed validations.
        :returns: The number of files that have failed validations.
    """
    # Verify that all required fields are not None
    for section in config.sections():
        for key, value in config[section].items():
            if key in REQUIRED and not value:
                print(f"--> WARNING: {key} is a required field and cannot be empty.")
                failures += 1

            if key == "branch_method" and value == "standard":
                for parent_key in PARENT_REQUIRED:
                    if config[section].get(parent_key) in (None, ""):
                        print(f"--> WARNING: {parent_key} is a required field and cannot be empty.")
                        failures += 1
            elif key == "branch_method" and value == "no parent":
                for parent_key in PARENT_REQUIRED:
                    if config[section].get(parent_key) not in (None, ""):
                        print(f"--> WARNING: {parent_key} is not required when using no parent branch method.")
                        failures += 1

            if key == "mass_data_class" and value == "ens" and not config[section].get("mass_ensemble_member"):
                print("--> WARNING: mass_ensemble_member is a required field and cannot be empty.")
                failures += 1
            if key == "mass_data_class" and value == "crum" and config[section].get("mass_ensemble_member"):
                print("--> WARNING: mass_ensemble_member is not needed when using 'crum' mass data class.")
                failures += 1

    return failures


def validate_field_inputs(config: configparser, failures: int) -> int:
    """
    Validates the inputs of a single .cfg file.

        :param config: The config parser.
        :param failures: The number of files that have failed validations.
        :returns: The number of files that have failed validations.
    """
    for section in config.sections():
        for key, value in config[section].items():
            # Verify datetime inputs
            if key == "branch_method" and value == "standard":
                DATETIME_FIELDS.append("branch_date_in_child")
                DATETIME_FIELDS.append("branch_date_in_parent")
            if key in DATETIME_FIELDS:
                if not re.compile(REGEX_FORMAT["datetime"]).fullmatch(value):
                    print(f"--> WARNING: {key} is an invalid datetime format.")
                    failures += 1

            # Verify workflow model ID structure
            if key == "model_workflow_id":
                if not re.compile(REGEX_FORMAT["model_workflow_id"]).fullmatch(value):
                    print(f"--> WARNING: {key} is incorrectly formatted.")
                    failures += 1

            # Verify variant label structure
            if key == "variant_label":
                if not re.compile(REGEX_FORMAT["variant_label"]).fullmatch(value):
                    print(f"--> WARNING: {key} is incorrectly formatted.")
                    failures += 1

            # Verify that atmospheric timestep is an integer
            if key == "atmos_timestep":
                if not value.isdigit() or int(value) < 0:
                    print(f"--> WARNING: {key} is invalid.")
                    failures += 1

            # Verify that no fields have the value "_No response_"
            if value == "_No response_":
                print(f"--> WARNING: {key} contains invalid entry ('_No response_').")
                failures += 1

    return failures


def main():
    """
    Holds the main body of the script.
    """
    config = configparser.ConfigParser()
    cfg_files = get_metadata_files()
    failed_files = []

    for file in cfg_files:
        failures = 0
        config.read(file)
        print(f"\nChecking {str(Path(file).stem)}.cfg")
        failures = validate_structure(config, file, failures)
        failures = Validate_required_fields(config, failures)
        failures = validate_field_inputs(config, failures)

        if failures != 0:
            failed_files.append(file)
        else:
            print("SUCCESS...")

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


if __name__ == "__main__":
    main()
