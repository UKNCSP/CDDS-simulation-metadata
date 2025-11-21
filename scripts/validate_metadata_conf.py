# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script scans all workflow metadata files and validates their structure and contents.
"""

from pathlib import Path
import glob
import configparser
from constants import SECTIONS, METADATA, DATA, MISC, REQUIRED, PARENT_REQUIRED, DATETIME_FIELDS
import re
import sys

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
    if not config.sections() == SECTIONS:
        print(f"--> WARNING: {str(Path(file).stem)}.cfg DOES NOT CONTAIN THE REQUIRED SECTIONS")
        unexpected = [s for s in config.sections() if s not in SECTIONS]
        missing = [s for s in SECTIONS if s not in config.sections()]
        if unexpected:
            print(f"    --> UNEXPECTED SECTIONS: {', '.join(unexpected)}")
        if missing:
            print(f"    --> MISSING SECTION: [{', '.join(missing)}]")
        failures += 1
        
        return failures

    # Verify the correct keys are in the correct section
    for section in SECTIONS:
        keys = list(config[section].keys())
        if section == 'metadata':
            target = METADATA
        elif section == 'data':
            target = DATA
        elif section == 'misc':
            target = MISC

        missing = [k for k in target if k not in keys]
        unexpected = [k for k in keys if k not in target]
        if missing or unexpected:
            print(f"--> WARNING: [{section}] DOES NOT CONTAIN THE REQUIRED KEYS")
            if missing:
                print(f"    --> MISSING KEYS: {', '.join(missing)}")
            if unexpected:
                print(f"    --> UNEXPECTED KEYS: {', '.join(unexpected)}")
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
    for section in SECTIONS:
        for key, value in config[section].items():
            if key in REQUIRED and value is None:
                print(f"--> WARNING: {key} IS A REQUIRED FIELD AND CANNOT BE EMPTY")
                failures +=1
            if key == "branch_method" and value == "standard":
                if key in PARENT_REQUIRED and value is None:
                    print(f"--> WARNING: {key} IS A REQUIRED FIELD AND CANNOT BE EMPTY")
                    failures += 1
            if key == "mass_data_class":
                if value == "ens":
                    if key == "mass_ensemble_member" and not value:
                        print(f"--> WARNING: {key} IS A REQUIRED FIELD AND CANNOT BE EMPTY")
                        failures += 1
                elif value == "crum":
                    if key == "mass_ensemble_member" and value:
                        print(f"--> WARNING: {key} IS NOT NEEDED WHEN USING CRUM MASS DATA CLASS")
                        failures += 1

    return failures


def validate_field_inputs(config: configparser, failures: int) -> int:
    """
    Validates the inputs of a single .cfg file.

        :param config: The config parser.
        :param failures: The number of files that have failed validations.
        :returns: The number of files that have failed validations.
    """
    for section in SECTIONS:
        for key, value in config[section].items():
            # Verify datetime inputs
            if key == "branch_method" and value == "standard":
                DATETIME_FIELDS.append("branch_date_in_child")
                DATETIME_FIELDS.append("branch_date_in_parent")
            format = r"^(?:\d{4})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\dZ$"
            format = re.compile(format)
            if key in DATETIME_FIELDS:
                if not format.fullmatch(value):
                    print(f"--> WARNING: {key} IS GIVEN IN AN INCORRECT DATETIME FORMAT")
                    failures += 1

            # Verify workflow model ID structure
            format = r"^[a-z]{1,2}-[a-z]{2}\d{3}$"
            format = re.compile(format)
            if key == "model_workflow_id":
                if not format.fullmatch(value):
                    print("-->WARNING: MODEL WORKFLOW ID IS INCORRECTLY FORMATTED")
                    failures += 1

            # Verify variant label structure
            format = r"^(r\d+)(i\d+[a-e]{0,1})(p\d+)(f\d+)$"
            format = re.compile(format)
            if key == "variant_label":
                if not format.fullmatch(value):
                    print("--> WARNING: VARIENT LABEL IS INCORRECTLY FORMATTED")
                    failures += 1
            
            # Verify that atmospheric timestep is an integer
            if key == "amtos_timestep":
                if not isinstance(value, int) or value < 0:
                    print("--> WARNING: ATMOSPHERIC TIMESTEP IS INVALID")
                    failures += 1

            # Verify that no fields have the value "_No response_"
            if value == "_No response_":
                print(f"--> WARNING: {key} CONTAINS AN INVALID ENTRY ('_No response_')")
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
    print(f"SUCCESSFULLY VALIDATED: {len(cfg_files)-len(failed_files)}/{len(cfg_files)}")
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