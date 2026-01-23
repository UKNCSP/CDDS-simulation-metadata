import unittest
import configparser
from pathlib import Path
import pytest

from scripts.validate_metadata_conf import validate_structure, validate_required_fields, validate_field_inputs

CONFIG = configparser.ConfigParser()
VALID_FILEPATH = Path("tests/test_scripts/data/valid_test_config.cfg")
INVALID_FILEPATH = Path("tests/test_scripts/data/invalid_test_config.cfg")


class TestValidateStructure(unittest.TestCase):

    def test_valid_structure(self):
        CONFIG.read(VALID_FILEPATH)
        result = {}
        result[VALID_FILEPATH] = {
            "file": VALID_FILEPATH,
            "failures": False,
        }
        valid_output = validate_structure(CONFIG, result, VALID_FILEPATH)
        msg = "A structurally valid configuration file is incorrectly being flagged as invalid"
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
        "unexpected fields")
        self.assertEqual(valid_output, result, msg)

    def test_missing_required_fields(self):
        CONFIG.read(INVALID_FILEPATH)
        result = {}
        result[INVALID_FILEPATH] = {
            "file": INVALID_FILEPATH,
            "failures": False,
        }
        invalid_output = validate_required_fields(CONFIG, result, INVALID_FILEPATH)
        print(invalid_output)
        expected = {
            INVALID_FILEPATH: {
                'file': INVALID_FILEPATH,
                'failures': True,
                'missing_values': ['branch_method'],
                'unexpected_values': ['mass_data_class']
            }
        }
        print(expected)
        msg = ("An invalid configuration file with missing or unexpected fields is not creating the expected error"
               f"dictionary...\nGot:\n{invalid_output}\nExpected:\n{expected}")
        self.assertEqual(invalid_output, expected, msg)


if __name__ == "__main__":
    unittest.main()
