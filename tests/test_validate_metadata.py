# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import unittest
from configparser import ConfigParser
from unittest.mock import patch

from scripts.validate_metadata import Validate


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "metadata": {
                "base_date": "1850-01-01T00:00:00Z",
                "branch_method": "standard",
                "branch_date_in_child": "1850-01-01T00:00:00Z",
                "branch_date_in_parent": "2000-01-01T00:00:00Z",
                "parent_experiment_id": "parent",
                "parent_mip": "PARENT_MIP",
                "parent_mip_era": "CMIP7",
                "parent_model_id": "UKCM2-0-LL",
                "parent_time_units": "days since 1850-01-01",
                "parent_variant_label": "r1i1p1f1",
                "calendar": "proleptic_gregorian",
                "experiment_id": "experiment",
                "institution_id": "INSTITUTION",
                "mip": "MIP",
                "mip_era": "CMIP7",
                "variant_label": "r1i1p1f1",
                "model_id": "UKCM2-0-LL",
            },
            "data": {
                "start_date": "2000-01-01T00:00:00Z",
                "end_date": "2001-01-01T00:00:00Z",
                "mass_data_class": "crum",
                "mass_ensemble_member": "",
                "model_workflow_id": "u-dx055",
            },
            "misc": {"atmos_timestep": "1800"},
        }
        self.validator = Validate(self.metadata)

    def test_config_to_dict(self):
        self.validator.errors.clear()
        config = ConfigParser()
        config.read_dict({"metadata": {"calendar": "360_day"}})

        converted = self.validator._config_to_dict(config)

        self.assertIsInstance(converted, dict, "Failed to convert configparser object to dict")
        self.assertEqual(converted["metadata"], {"calendar": "360_day"}, "Failed to correcty structure metadata dict")

    def test_set_invalid_calendar(self):
        self.validator.errors.clear()
        self.metadata["metadata"]["calendar"] = "invalid"
        self.validator.set_calendar()
        expected_msg = "incompatible calendar: expected 360_day or proleptic_gregorian"
        self.assertEqual(self.validator.errors["calendar"], expected_msg, "Failed to flag invalid calendar")

    def test_check_missing_inputs(self):
        self.validator.errors.clear()
        self.metadata["metadata"]["institution_id"] = ""
        self.metadata["misc"]["atmos_timestep"] = "_No response_"
        self.validator.check_for_missing_inputs()
        self.assertCountEqual(
            self.validator.errors["missing_required_field"],
            ["Missing field institution_id", "Missing field atmos_timestep"],
        )

    def test_check_parent_fields(self):
        self.validator.errors.clear()
        self.validator.check_parent_fields()
        self.assertEqual(self.validator.errors, {})

        self.metadata["metadata"]["parent_mip"] = ""
        self.validator.check_parent_fields()
        self.assertEqual(self.validator.errors["missing_parent_field"], ["missing required parent field: parent_mip"])

        self.validator.errors.clear()
        self.metadata["metadata"]["branch_method"] = "no parent"
        self.metadata["metadata"]["branch_date_in_child"] = ""
        self.metadata["metadata"]["branch_date_in_parent"] = ""
        self.metadata["metadata"]["parent_experiment_id"] = ""
        self.metadata["metadata"]["parent_mip"] = "PARENT_MIP"
        self.metadata["metadata"]["parent_mip_era"] = ""
        self.metadata["metadata"]["parent_model_id"] = ""
        self.metadata["metadata"]["parent_time_units"] = ""
        self.metadata["metadata"]["parent_variant_label"] = ""

        self.validator.check_parent_fields()
        self.assertEqual(self.validator.errors["unexpected_parent_field"], ["unexpected field: parent_mip"])

    def test_check_mass_data_class(self):
        self.validator.errors.clear()
        self.validator.check_mass_data_class_attributes()
        self.assertEqual(self.validator.errors, {})

        self.metadata["data"]["mass_data_class"] = "ens"
        self.validator.check_mass_data_class_attributes()
        self.assertEqual(self.validator.errors["missing_mass_field"], "missing field: mass_ensemble_member")

        self.metadata["data"]["mass_data_class"] = "crum"
        self.metadata["data"]["mass_ensemble_member"] = "r1"
        self.validator.check_mass_data_class_attributes()
        self.assertEqual(self.validator.errors["unexpected_mass_field"], "unexpected field: mass_ensemble_member")

    def test_normalise_datetime(self):
        self.validator.errors.clear()
        self.assertEqual(self.validator.normalise_datetime("2000-01-01T00:00:00Z", "start_date"),
                         "2000-01-01T00:00:00Z")
        self.assertEqual(self.validator.errors, {})

        self.validator.normalise_datetime("not-a-date", "start_date")
        self.assertEqual(self.validator.errors["datetime"], "invalid datetime format for start_date")

    def test_check_datetime_fields(self):
        self.validator.errors.clear()
        self.validator.check_datetime_fields()
        self.assertEqual(self.metadata["data"]["start_date"], "2000-01-01T00:00:00Z")

        self.metadata["data"]["start_date"] = "not-a-date"
        self.validator.check_datetime_fields()
        self.assertEqual(self.validator.errors["datetime"], "invalid datetime format for start_date")

    def test_check_model_workflow_ids(self):
        self.validator.errors.clear()
        self.validator.check_model_workflow_id()
        self.assertEqual(self.validator.errors, {})

        self.metadata["data"]["model_workflow_id"] = "invalid"
        self.validator.check_model_workflow_id()
        self.assertEqual(self.validator.errors["workflow_id_format"],
                         "model workflow ID is incorrectly formatted: expected a-bc123 or ab-cd123")

    def test_check_variant_labels(self):
        self.validator.errors.clear()
        self.validator.check_variant_labels()
        self.assertEqual(self.validator.errors, {})

        self.metadata["metadata"]["parent_variant_label"] = "invalid"
        self.validator.check_variant_labels()
        expected_msg = "variant label or parent variant label is incorrectly formatted: expected r1i1p1f1 like format"
        self.assertEqual(self.validator.errors["label_format"], expected_msg)

    def test_check_atmos_timestep(self):
        self.validator.errors.clear()
        self.validator.check_atmos_timestep()
        self.assertEqual(self.validator.errors, {})

        self.metadata["misc"]["atmos_timestep"] = "1800s"
        self.validator.check_atmos_timestep()
        self.assertEqual(self.validator.errors["timestep_logic"], "atmospheric timestep is invalid")

    def test_check_start_end_logic(self):
        self.validator.errors.clear()
        self.validator.check_start_end_logic()
        self.assertEqual(self.validator.errors, {})

        self.metadata["data"]["start_date"] = "2010-01-01T00:00:00Z"
        self.validator.check_start_end_logic()
        self.assertEqual(self.validator.errors["datetime_logic"], "end date cannot be earlier than start date")

        self.validator.errors.clear()
        self.metadata["data"]["start_date"] = "1849-01-01T00:00:00Z"
        self.validator.check_start_end_logic()
        self.assertEqual(self.validator.errors["datetime_logic"],
                         "Start date cannot be earlier than the base date: 1850-01-01")

    def test_check_fixed_fields(self):
        self.validator.errors.clear()
        self.validator.check_fixed_fields()
        self.assertEqual(self.validator.errors, {})

        self.metadata["metadata"]["model_id"] = "unknown"
        self.metadata["metadata"]["parent_model_id"] = "different"
        self.validator.check_fixed_fields()
        self.assertIn("unrecognised_input", self.validator.errors)
        self.assertIn("model_id must have the value 'UKCM2-0-LL', 'UKCM2a-0-HH', 'UKESM1-3-LL' or 'HadGEM3-GC31-MM'",
                      self.validator.errors["unrecognised_input"])

    def test_check_cvs(self):
        self.validator.errors.clear()
        cv = {
            "CV": {
                "institution_id": ["INSTITUTION"],
                "experiment_id": {
                    "experiment": {
                        "activity_id": ["MIP"],
                        "parent_experiment_id": ["parent"],
                        "parent_activity_id": ["PARENT_MIP"],
                        "end_year": "2000",
                    }
                },
            }
        }
        with patch("scripts.validate_metadata.CMOR_CV_JSON", cv):
            self.validator.check_cvs()
            self.assertEqual(self.validator.errors, {})
            self.assertEqual(self.validator.warnings, {})

            self.metadata["metadata"]["experiment_id"] = "missing"
            self.validator.errors.clear()
            self.validator.check_cvs()
            self.assertEqual(self.validator.errors["cv_error"],
                             ["experiment id 'missing' could not be found in the cvs"])

    @unittest.skip("This is a wrapper function which calls functions tested above. Skipping test to avoid duplicates")
    def test_validate_all(self):
        pass
