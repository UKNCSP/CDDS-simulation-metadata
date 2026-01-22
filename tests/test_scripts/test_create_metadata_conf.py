import unittest
from pathlib import Path
import json
from textwrap import dedent

from scripts.create_metadata_conf import (set_calendar, process_metadata, validate_meta_content, format_warning_message,
                                          sort_to_categories)


class TestSetCalendar(unittest.TestCase):

    def test_valid_calendars(self):
        self.assertEqual(set_calendar("360_day"), {}, "Unable to successfully set the calendar to 360_day")
        self.assertEqual(set_calendar("gregorian"), {}, "Unable to successfully set the calendar to gregorian")

    def test_invalid_calendar(self):
        calendar_output = set_calendar("not_a_calendar")
        expected = {"calendar": "Incompatible calendar: expected 360_day or gregorian"}
        msg = (f"An valid calendar is not resulting in the expected error message:\nExpected:\n{expected}\nGot:\n"
               f"{calendar_output}")
        self.assertEqual(calendar_output, expected, msg)


class TestProcessMetadata(unittest.TestCase):

    def test_process_metadata(self):
        match = [('Issue Type', 'New'), ('Model Workflow ID', 'u-dv623'), ('Activity ID (MIP)', 'CMIP'),
                 ('Experiment ID', '1pctCO2'), ('Model ID', 'UKCM2-LL'), ('Variant label', 'r2i1p1f1'),
                 ('Start Date', '1850-01-01T00:00:00Z'), ('End Date', '2000-01-01T00:00:00Z'),
                 ('Base Date', '1850-01-01T00:00:00Z'), ('Branch Method', 'standard'), ('Calendar Type', 'gregorian'),
                 ('Institution ID', 'MOHC'), ('MIP Era', 'CMIP7'), ('Atmospheric Timestep', '1800'),
                 ('Mass Data Class', 'crum'), ('Child Branch Date', '1850-01-01T00:00:00Z'),
                 ('Parent Branch Date', '1850-01-01T00:00:00Z'), ('Parent Experiment ID', 'piControl'),
                 ('Parent Activity ID (MIP)', 'CMIP'), ('Parent Model ID', 'UKCM2-LL'),
                 ('Parent Time Units', 'days since 1850-01-01'), ('Parent Variant Label', 'r1i1p1f1'),
                 ('Mass Ensemble Member ID', '_No response_')]
        with open(Path("tests/test_scripts/data/expected_outputs/process_metadata.json"), "r") as fh:
            expected = json.load(fh)

        processed_metadata = process_metadata(match)
        msg = "The issue body has not been processed correctly into a dictionary format."
        self.assertEqual(processed_metadata, expected, msg)


class TestValidateMetaContent(unittest.TestCase):

    def test_successful_validation(self):
        with open(Path("tests/test_scripts/data/inputs/valid_meta_dict.json"), "r") as fh:
            valid_meta_dict = json.load(fh)

        errors = validate_meta_content(valid_meta_dict)
        msg = "A valid dictionary is incorrectly failing validation."
        self.assertEqual(errors, {}, msg)

    def test_unsuccessful_validation(self):
        with open(Path("tests/test_scripts/data/inputs/faulty_meta_dict.json"), "r") as fh:
            faulty_meta_dict = json.load(fh)
        with open(Path("tests/test_scripts/data/expected_outputs/errors_dict.json"), "r") as fh:
            expected = json.load(fh)

        errors = validate_meta_content(faulty_meta_dict)
        msg = "Validation of an invalid dictionary is not producing the expected error flags."
        self.assertEqual(errors, expected, msg)


class TestFormatWarningMessage(unittest.TestCase):

    def test_format_warning_message(self):
        with open(Path("tests/test_scripts/data/expected_outputs/errors_dict.json"), "r") as fh:
            errors_dict = json.load(fh)
        expected = ("Missing parent field warning (missing required parent field: parent mip).\nMissing required field "
        "warning (missing field experiment id).\nLabel format warning (variant label is incorrectly formatted: "
        "expected r1i1p1f2 like format).\nUnexpected mass field warning (unexpected field: mass data class).\n"
        "Workflow id format warning (model workflow id is incorrectly formatted: expected a-bc123).\nTimestep logic "
        "warning (atmospheric timestep is invalid).\nDatetime logic warning (end date cannot be earlier than start "
        "date).")

        warning_message = format_warning_message(errors_dict)
        msg = (f"The error message provided to the user is not being formated as expected.\nExpected:\n"
               f"'{dedent(expected)}'\nGot:\n'{warning_message}'\n")
        self.assertEqual(warning_message, dedent(expected), msg)


class TestSortToCategories(unittest.TestCase):

    def test_sort_to_categories(self):
        with open(Path("tests/test_scripts/data/inputs/valid_meta_dict.json"), "r") as fh:
            meta_dict = json.load(fh)
        with open(Path("tests/test_scripts/data/expected_outputs/organised_categories.json"), "r") as fh:
            expected = json.load(fh)

        sorted_dict = sort_to_categories(meta_dict)
        msg = (f"Metadata could not be correctly sorted into the required categories.\nExpected:\n{expected}\nGot:\n"
               f"{sorted_dict}")
        self.assertEqual(sorted_dict, expected, msg)


if __name__ == '__main__':
    unittest.main()
