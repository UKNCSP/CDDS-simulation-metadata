# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest
import os

from unittest.mock import mock_open, patch

from scripts.common import read_json, get_issue, process_metadata, format_message


class TestReadJson(unittest.TestCase):
    def test_read_json(self):
        mock_json = '{"foo": "bar"}'
        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = read_json("mock_json.json")

        self.assertEqual(result, {"foo": "bar"}, "Failed to read source JSON file.")
        self.assertIsInstance(result, dict,
                              f"JSON file content returned as incorrect type, expected dict, got {type(result)}")

    def test_read_list_json(self):
        mock_json = '[{"foo": "bar"}, {"baz": "bing"}]'
        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = read_json("mock_json.json")

        msg = f"JSON file content returned as incorrect type, expected list, got {type(result)}"
        self.assertIsInstance(result, list, msg)


class TestGetIssue(unittest.TestCase):
    def test_get_issue_success(self):
        os.environ = {"ISSUE_BODY": "foo"}
        self.assertEqual(get_issue(), {"body": "foo"}, "Failed to extract issue body from environment variable")

    def test_get_issue_failure(self):
        os.environ = {"ISSUE_TITLE": "bar"}
        self.assertEqual(get_issue(), {"body": None}, "Incorrectly identified issue body when none exists")


class TestProcessMetadata(unittest.TestCase):
    def test_process_metadata(self):
        metadata = [
            ("Base date", "1850-01-01T00:00:00Z"), ("Branch method", "no parent"),
            ("Child branch date", "_No response_"), ("Parent branch date", "_No response_"),
            ("Parent experiment id", "_No response_"), ("Parent activity id (mip)", "_No response_"),
            ("Parent mip era", "_No response_"), ("Parent model id", "_No response_"),
            ("Parent time units", "_No response_"), ("Parent variant label", "_No response_"),
            ("Calendar type", "360_day"), ("Experiment id", "1pctCO2"), ("Institution id", "UKNCSP"),
            ("Activity id (mip)", "CMIP"), ("Mip era", "CMIP7"), ("Variant label", "r1i1p1f1"),
            ("Model id", "UKCM2-0-LL"), ("Start date", "1850"), ("End date", "2100"), ("Mass data class", "crum"),
            ("Mass ensemble member id", "_No response_"), ("Model workflow id", "a-bc123"),
            ("Atmospheric timestep", "1200")
        ]
        expected = {
            "base_date": "1850-01-01T00:00:00Z",
            "branch_method": "no parent",
            "branch_date_in_child": "",
            "branch_date_in_parent": "",
            "parent_experiment_id": "",
            "parent_mip": "",
            "parent_mip_era": "",
            "parent_model_id": "",
            "parent_time_units": "",
            "parent_variant_label": "",
            "calendar": "360_day",
            "experiment_id": "1pctCO2",
            "institution_id": "UKNCSP",
            "mip": "CMIP",
            "mip_era": "CMIP7",
            "variant_label": "r1i1p1f1",
            "model_id": "UKCM2-0-LL",
            "start_date": "1850",
            "end_date": "2100",
            "mass_data_class": "crum",
            "mass_ensemble_member": "",
            "model_workflow_id": "a-bc123",
            "atmos_timestep": "1200"
        }
        result = process_metadata(metadata)
        self.maxDiff = None
        self.assertEqual(result, expected, "Failed to process issue form content into a dictionary.")


class TestFormatMessage(unittest.TestCase):
    def test_format_message(self):
        err_msg_result = format_message({"error_message": "This is an error message"}, "error")
        err_msg_expected = "Error message error: This is an error message."

        warn_msg_result = format_message({"warning_message": "This is an warning message"}, "warning")
        warn_msg_expected = "Warning message warning: This is an warning message."

        self.assertEqual(err_msg_result, err_msg_expected, "Failed to correctly format error message")
        self.assertEqual(warn_msg_result, warn_msg_expected, "Failed to correctly format warning message")


if __name__ == '__main__':
    unittest.main()
