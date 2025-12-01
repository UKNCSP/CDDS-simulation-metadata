# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.
"""
This script takes the body of an issue and uses its content to generate a structured metadata configuration file.

The issue body content generated from an issue form is cleaned, validated and sorted into the required formatting for
metadata cfg files. This is then passed on into a workflow as an output file along with any errors that may have been
flagged.
"""

import os
import re
import sys
from pathlib import Path

from constants import (
    DATA,
    DATETIME_FIELDS,
    META_FIELDS,
    METADATA,
    MISC,
    PARENT_REQUIRED,
    REGEX_FORMAT,
    REQUIRED,
)
from metomi.isodatetime.data import Calendar
from metomi.isodatetime.parsers import TimePointParser

REGEX_DICT = {
    "datetime_pattern": re.compile(REGEX_FORMAT["datetime"]),
    "workflow_pattern": re.compile(REGEX_FORMAT["model_workflow_id"]),
    "variant_pattern": re.compile(REGEX_FORMAT["variant_label"]),
}

ACCEPTED_DATETIME_PATTERNS = re.compile(
    r"(\d{4})"
    r"(?:-(\d{2}))?"
    r"(?:-(\d{2}))?"
    r"(?:T(\d{2}))?"
    r"(?::(\d{2}))?"
    r"(?::(\d{2}))?"
    r"(?:Z)?"
)


def get_issue() -> dict[str, str]:
    """
    Extracts the issue body from the submitted issue form.

    :returns: The issue body as a dictionary.
    """
    return {
        "body": os.environ.get("ISSUE_BODY"),
    }


def normalise_datetime(field: str) -> str:
    """
    Populates undefined datetime fields with default values to match yyyy-mm-ddTHH:MM:SSZ formatting.

    :param field: The datetime string to be reformatted.
    :returns: The normalised datetime string in the of format yyyy-mm-ddTHH:MM:SSZ.
    """
    match = ACCEPTED_DATETIME_PATTERNS.findall(field)
    if match:
        year, month, day, hour, minute, second = match[0]

    # Reformat and normalise string.
    default = {
        "YYYY": year,
        "MM": month or "01",
        "DD": day or "01",
        "hh": hour or "00",
        "mm": minute or "00",
        "ss": second or "00",
    }
    normalised_time_str = "{YYYY}-{MM}-{DD}T{hh}:{mm}:{ss}Z".format(**default)

    return normalised_time_str


def process_metadata(match: list[tuple[str]]) -> dict[str, str]:
    """
    Generates a dictionary from the loaded issue body and cleans the contents to ensure consistent formatting.

    :param match: The identified key-value pairs from the issue body.
    :returns: A cleaned dictionary containing the metadata keys and values from the issue form.
    """
    meta_dict = {}

    # Clean parsed data
    for key, value in set(match):
        clean = key.strip().lower().replace(" ", "_")
        meta_dict[clean] = value.strip()
    # Re map keys to correct CV format
    for old_key, new_key in META_FIELDS.items():
        meta_dict[new_key] = meta_dict.pop(old_key)

    for key, value in meta_dict.items():
        # Reformat blank fields.
        if meta_dict[key] == "_No response_":
            meta_dict[key] = ""
        # Convert all accepted fields to yyyy-mm-ddTHH:MM:SSZ format.
        if key in DATETIME_FIELDS:
            meta_dict[key] = normalise_datetime(meta_dict[key])

    return meta_dict


def set_calendar(calendar_type: str) -> dict[str, str]:
    """
    Sets the metomi.isodatetime calendar.

    :param calendar_type: The type of calendar used.
    :returns: A dictionary containing any errors caused by user input from the form.
    """
    errors = {}

    if calendar_type == "360_day" or calendar_type == "gregorian":
        Calendar.default().set_mode(calendar_type)
        pass
    else:
        errors["calendar"] = "Incompatible calendar: expected 360_day or gregorian"

    return errors


def validate_meta_content(meta_dict: dict[str, str]) -> dict[str, str]:
    """
    Validates the metadata dictionary contents.

    :param meta_dict: A cleaned dictionary containing the metadata keys and values from the issue form.
    :returns: A dictionary containing any errors caused by user input from the form.
    """
    errors = set_calendar(meta_dict["calendar"])
    # Confirm that conditional fields are present.
    for key, value in meta_dict.items():
        if key in REQUIRED and not value:
            errors["missing_required_field"] = f"Missing field {key}"

        if key == "mass_data_class":
            if value == "ens" and not meta_dict.get("mass_ensemble_member"):
                errors["missing_mass_field"] = f"Missing field: {key}"
            if value == "crum" and meta_dict.get("mass_ensemble_member"):
                errors["unexpected_mass_field"] = f"Unexpected field: {key}"

        if key == "branch_method":
            if value == "standard":
                for parent_key in PARENT_REQUIRED:
                    if meta_dict.get(parent_key) in (None, "", "_No response_"):
                        errors["missing_parent_field"] = f"Missing required parent field: {parent_key}"
            elif value == "no parent":
                for parent_key in PARENT_REQUIRED:
                    if meta_dict.get(parent_key) not in (None, "", "_No response_"):
                        errors["unexpected_parent_field"] = (f"Unexpected field: {parent_key}")

        # Verify datetime inputs
        parser = TimePointParser()
        if key == "branch_method" and value == "standard":
            DATETIME_FIELDS.add("branch_date_in_child")
            DATETIME_FIELDS.add("branch_date_in_parent")
        if key in DATETIME_FIELDS and not REGEX_DICT["datetime_pattern"].fullmatch(value):
            errors["datetime_format"] = (f"{key} is incorrectly formatted: expected yyyy-mm-ddTHH:MM:SSZ")

        # Confirm that end_time is not earlier than start_time.
        if parser.parse(meta_dict["end_date"]) < parser.parse(meta_dict["start_date"]):
            errors["datetime_logic"] = ("WARNING: end date cannot be earlier than start date")

        # Verify workflow model ID structure
        if key == "model_workflow_id" and not REGEX_DICT["workflow_pattern"].fullmatch(value):
            errors["workflow_id_format"] = ("Model workflow ID is incorrectly formatted: expected a-bc123")

        # Verify variant label structure
        if key == "variant_label" and not REGEX_DICT["variant_pattern"].fullmatch(value):
            errors["label_format"] = ("Variant label is incorrectly formatted: expected r1i1p1f2")

        # Verify that atmospheric timestep is an integer
        if key == "atmos_timestep" and (not value.isdigit() or int(value) < 0):
            errors["timestep_logic"] = "Atmospheric timestep is invalid"

    return errors


def format_warning_message(errors: dict[str, str]) -> str:
    """
    Formats the a human readable warning message to be returned to the user.

    :param errors: A dictionary containing any errors caused by user input from the form.
    :returns: A human readable message detailing all warnings.
    """
    warnings = []
    for key, value in errors.items():
        clean_key = key.strip().capitalize().replace("_", " ")
        clean_value = value.strip().lower().replace("_", " ")
        warning = clean_key + " warning " + "(" + clean_value + ")."
        warnings.append(warning)

    warnings = "\n".join(warnings)

    return warnings


def create_filename(meta_dict: dict[str, str]) -> str:
    """
    Generates a filename based off of the input model workflow id and mass ensemble member.

    :param meta_dict: A cleaned dictionary containing the metadata keys and values from the issue form.
    :returns: The name of the metadata configuration file.
    """
    model_workflow_id = meta_dict["model_workflow_id"]
    if meta_dict["mass_data_class"] == "ens":
        mass_ensemble_member_id = meta_dict["mass_ensemble_member"]
        filename = f"{model_workflow_id}-{mass_ensemble_member_id}.cfg"
    else:
        filename = f"{model_workflow_id}.cfg"

    return filename


def sort_to_categories(meta_dict: dict[str, str]) -> dict[dict[str, str]]:
    """
    Sorts the metadata dictionary into appropriate categories as nested dictionaries.

    :param meta_dict: A cleaned dictionary containing the metadata keys and values from the issue form.
    :returns: A cleaned, organised dictionary containing the validated metadata keys and values from the issue form.
    """
    metadata_dict = {}
    data_dict = {}
    misc_dict = {}
    organised_metadata = {}

    # Categorise keys into sections that match the request.cfg mapping.
    for key, value in meta_dict.items():
        if key in METADATA:
            metadata_dict[key] = value
        elif key in DATA:
            data_dict[key] = value
        elif key in MISC:
            misc_dict[key] = value

    # Re map organised keys as nested dictionaries.
    organised_metadata["[metadata]"] = metadata_dict
    organised_metadata["[data]"] = data_dict
    organised_metadata["[misc]"] = misc_dict

    return organised_metadata


def format_cfg_file(output_file: Path, organised_metadata: dict[str, str]) -> None:
    """
    Writes the cleaned, organised and validated metadata to a structured configuration file.

    :param output_file: The complete path of the output file.
    :param organised_metadata: A cleaned, organised dictionary containing the validated metadata keys and values from
                               the issue form.
    """
    with open(output_file, "w") as f:
        for key, value in organised_metadata.items():
            f.write(f"{key}\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    f.write(f"{k} = {v}\n")
                f.write("\n")


def main() -> None:
    """
    Holds the main body of the script.
    """
    issue_body = get_issue()['body']

    # Find key-value pairs and map them to dictionary process.
    match = re.findall(r"### (.+?)\n\s*\n?(.+)", issue_body)
    meta_dict = process_metadata(match)
    print("Extracting issue body...  SUCCESSFUL")

    # Validate and organise dictionary content.
    errors = validate_meta_content(meta_dict)
    organised_metadata = sort_to_categories(meta_dict)

    # Create output file.
    filename = create_filename(meta_dict)

    if not errors:
        print("Validating issue form inputs...  SUCCESSFUL")
        output_dir = Path("workflow_metadata")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{filename}"

        with open(os.environ["GITHUB_OUTPUT"], "a") as gh:
            gh.write(f"filename={output_file}")

        format_cfg_file(output_file, organised_metadata)
        print(f"Saving metadata file as {output_file}...  SUCCESSFUL")

    else:
        print("Validating issue form inputs...  FAILED")
        warnings = format_warning_message(errors)

        with open(os.environ["GITHUB_OUTPUT"], "a") as gh:
            gh.write(f"warnings={warnings}")

        sys.exit(1)


if __name__ == "__main__":
    main()
