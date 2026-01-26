import unittest
import configparser
from pathlib import Path
import pytest
import collections

from scripts.validate_metadata_conf import validate_structure, validate_required_fields, validate_field_inputs

CONFIG = configparser.ConfigParser()
TEST_DATA_DIR = Path("tests/test_scripts/data")
VALID_FILEPATH = Path(TEST_DATA_DIR / "valid_test_config.cfg")
INVALID_FILEPATH = Path(TEST_DATA_DIR / "invalid_test_config.cfg")


class TestValidateStructure(unittest.TestCase):

    def test_valid_structure(self):
        CONFIG.read(VALID_FILEPATH)
        result = {}
        result[VALID_FILEPATH] = {
            "file": VALID_FILEPATH,
            "failures": False,
        }
        valid_output = validate_structure(CONFIG, result, VALID_FILEPATH)
        msg = "A structurally valid configuration file is incorrectly being flagged as invalid."
        self.assertEqual(valid_output, result, msg)

    @pytest.mark.xfail()
    def test_invalid_structure(self):
        CONFIG.read(INVALID_FILEPATH)
        result = {}
        result[INVALID_FILEPATH] = {
            "file": INVALID_FILEPATH,
            "failures": False,
        }
        invalid_output = validate_structure(CONFIG, result, INVALID_FILEPATH)
        expected = {
            INVALID_FILEPATH: {
                'file': INVALID_FILEPATH,
                'failures': True,
                'missing_sections': ['misc'],
                'unexpected_sections': ['unexpected'],
                'missing_keys': ['mip'],
                'unexpected_keys': ['atmos_timestep']
            }
        }
        msg = ("A structurally invalid configuration file is not creating the expected error dictionary...\nGot:\n"
               f"{invalid_output}\nExpected:\n{expected}")
        self.assertEqual(invalid_output, expected, msg)


class TestValidateRequiredFields(unittest.TestCase):

    def test_all_required_fields(self):
        CONFIG.read(VALID_FILEPATH)
        result = {}
        result[VALID_FILEPATH] = {
            "file": VALID_FILEPATH,
            "failures": False,
        }
        valid_output = validate_required_fields(CONFIG, result, VALID_FILEPATH)
        msg = ("A configuration file contianing all required fields is incorrectly being flagged as having missing or "
        "unexpected fields.")
        self.assertEqual(valid_output, result, msg)

    def test_missing_required_fields(self):
        CONFIG.read(INVALID_FILEPATH)
        result = {}
        result[INVALID_FILEPATH] = {
            "file": INVALID_FILEPATH,
            "failures": False,
        }
        invalid_output = validate_required_fields(CONFIG, result, INVALID_FILEPATH)
        expected = {
            INVALID_FILEPATH: {
                'file': INVALID_FILEPATH,
                'failures': True,
                'missing_values': ['branch_method'],
                'unexpected_values': ['mass_data_class']
            }
        }
        msg = ("An invalid configuration file with missing or unexpected fields is not creating the expected error "
               f"dictionary...\nGot:\n{invalid_output}\nExpected:\n{expected}")
        self.assertEqual(invalid_output, expected, msg)


class TestValidateFieldInputs(unittest.TestCase):

    def test_valid_field_inputs(self):
        CONFIG.read(VALID_FILEPATH)
        result = {}
        result[VALID_FILEPATH] = {
            "file": VALID_FILEPATH,
            "failures": False,
        }
        valid_output = validate_field_inputs(CONFIG, result, VALID_FILEPATH)
        msg = "A valid field within the configuration file is incorrectly being flagged as invalid."
        self.assertEqual(valid_output, result, msg)

    def test_invalid_field_inputs(self):
        CONFIG.read(INVALID_FILEPATH)
        result = {}
        result[INVALID_FILEPATH] = {
            "file": INVALID_FILEPATH,
            "failures": False,
        }
        invalid_output = validate_field_inputs(CONFIG, result, INVALID_FILEPATH)
        expected = ['branch_date_in_parent', 'institution_id', 'variant_label', 'branch_date_in_child',
                                   'model_workflow_id', 'atmos_timestep']
        msg = (f"An invalid field entry is not creating the expected error dictionary...\nGot:\n{invalid_output}\n"
               f"Expected:\n{expected}")
        self.assertEqual(collections.Counter(invalid_output[INVALID_FILEPATH]['invalid_values']),
                         collections.Counter(expected), msg)


if __name__ == "__main__":
    unittest.main()
