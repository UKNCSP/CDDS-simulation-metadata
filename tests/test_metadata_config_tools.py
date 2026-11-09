# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest

from unittest.mock import mock_open, patch

from scripts.metadata_config_tools import MetadataConfigTools
from scripts.constants import WORKFLOW_METADATA_DIR


class TestMetadataConfigTools(unittest.TestCase):
    def setUp(self):
        self.mock_config = (
            "[metadata]\n"
            "base_date = 1850-01-01T00:00:00Z\n"
            "branch_method = standard\n"
            "branch_date_in_child = 1850-01-01T00:00:00Z\n"
            "branch_date_in_parent = 2100-01-01T00:00:00Z\n"
            "parent_experiment_id = piControl\n"
            "parent_mip = CMIP\n"
            "parent_mip_era = CMIP7\n"
            "parent_model_id = UKCM2-0-LL\n"
            "parent_time_units = days since 1850-01-01\n"
            "parent_variant_label = r1i1p1f1\n"
            "calendar = proleptic_gregorian\n"
            "experiment_id = historical\n"
            "institution_id = UKNCSP\n"
            "mip = CMIP\n"
            "mip_era = CMIP7\n"
            "variant_label = r1i1p1f1\n"
            "model_id = UKCM2-0-LL\n\n"
            "[data]\n"
            "start_date = 1850-01-01T00:00:00Z\n"
            "end_date = 2022-01-01T00:00:00Z\n"
            "mass_data_class = crum\n"
            "mass_ensemble_member =\n"
            "model_workflow_id = u-dx055\n\n"
            "[misc]\n"
            "atmos_timestep = 1800\n\n"
            "[ADDITIONAL INFO]\n"
            "notes =\n"
            "updates =\n"
        )
        self.metadata = MetadataConfigTools("u-dx055")

        return self

    def test_read_config_success(self):
        with patch("builtins.open", mock_open(read_data=self.mock_config)):
            result = self.metadata.read_config()
        self.assertIs(result, self.metadata)

    def test_read_config_missing_file(self):
        workflow_id = "invalid"
        file_path = f"{WORKFLOW_METADATA_DIR}/{workflow_id}.cfg"
        with patch("scripts.metadata_config_tools.ConfigParser") as config_parser:
            parser = config_parser.return_value
            parser.__bool__.return_value = False
            with self.assertRaises(FileNotFoundError) as context:
                MetadataConfigTools(workflow_id).read_config()
        self.assertEqual(str(context.exception), f"{file_path} does not exist.")

    def test_set_calendar(self):
        with patch("builtins.open", mock_open(read_data=self.mock_config)):
            self.metadata.read_config()

        # Confirm that valid calendars are set successfully.
        self.metadata.config["metadata"]["calendar"] = "proleptic_gregorian"
        self.assertEqual(self.metadata.set_calendar(), None, "Failed to set calendar as `gregorian`")
        self.metadata.config["metadata"]["calendar"] = "360_day"
        self.assertEqual(self.metadata.set_calendar(), None, "Failed to set calendar as `360_day`")

        # Confirm that invalid calendar raises error
        self.metadata.config["metadata"]["calendar"] = "invalid"
        with self.assertRaises(RuntimeError) as context:
            self.metadata.set_calendar()
        self.assertEqual(str(context.exception), f"Unrecognsied calendar: {self.metadata._calendar}")

    def test_section_properties(self):
        with patch("builtins.open", mock_open(read_data=self.mock_config)):
            self.metadata.read_config()

        self.assertEqual(self.metadata._metadata_section, self.metadata.config["metadata"],
                         "Failed to identify metadata section")
        self.assertEqual(self.metadata._data_section, self.metadata.config["data"], "Failed to identify data section")
        self.assertEqual(self.metadata._misc_section, self.metadata.config["misc"], "Failed to identify misc section")
        self.assertEqual(self.metadata._additional_info_section, self.metadata.config["ADDITIONAL INFO"],
                         "Failed to identify additional info section")

    def test_keys_properties(self):
        with patch("builtins.open", mock_open(read_data=self.mock_config)):
            self.metadata.read_config()

        self.assertEqual(self.metadata._mip_era, self.metadata.config["metadata"]["mip_era"],
                         "Failed to identify mip_era")
        self.assertEqual(self.metadata._drs_specs, "MIP-DRS7",
                         f"Failed to identify drs_specs for {self.metadata._mip_era}")
        self.assertEqual(self.metadata._mip, self.metadata.config["metadata"]["mip"],
                         "Failed to identify mip")
        self.assertEqual(self.metadata._institution_id, self.metadata.config["metadata"]["institution_id"],
                         "Failed to identify institution_id")
        self.assertEqual(self.metadata._model_id, self.metadata.config["metadata"]["model_id"],
                         "Failed to identify model_id")
        self.assertEqual(self.metadata._experiment_id, self.metadata.config["metadata"]["experiment_id"],
                         "Failed to identify experiment_id")
        self.assertEqual(self.metadata._variant_label, self.metadata.config["metadata"]["variant_label"],
                         "Failed to identify variant_label")
        self.assertEqual(self.metadata._calendar, self.metadata.config["metadata"]["calendar"],
                         "Failed to identify calendar")
        self.assertEqual(int(self.metadata._run_length_years), 172, "Failed to calculate run length")
