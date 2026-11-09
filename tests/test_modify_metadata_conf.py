# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import unittest
import tempfile
import configparser

from datetime import datetime

from scripts.modify_metadata_conf import (read_issue_body, read_metadata_file, identify_changes,
                                          identify_config_section, log_update)


@unittest.skip("Skip for now. This function is difficult to test since variables are defined internally.")
class TestReadIssueBody(unittest.TestCase):
    def test_read_issue_body(self):
        pass


class TestReadMetadataFile(unittest.TestCase):
    def test_read_metadata_file(self):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as file:
            file.write("[metadata]\nmodel_id = test\n")
            file.flush()
            config = read_metadata_file(file.name)
        self.assertEqual(config["metadata"]["model_id"], "test")

    def test_file_not_found(self):
        filename = "nonexistant.txt"
        with self.assertRaises(FileNotFoundError) as context:
            read_metadata_file(filename)
        self.assertEqual(str(context.exception), f"{filename} does not exist.")


class TestIdentifyChanges(unittest.TestCase):
    def test_identify_changes(self):
        meta_dict = {
            "experiment_id": "test",
            "model_workflow_id": "test"
        }
        self.assertEqual(identify_changes(meta_dict), [{"experiment_id": "test"}])


class TestIdentifyConfigSection(unittest.TestCase):
    def test_identify_metadata_section(self):
        self.assertEqual(identify_config_section("experiment_id"), "metadata", "Failed to identify metadata section")

    def test_identify_data_section(self):
        self.assertEqual(identify_config_section("start_date"), "data", "Failed to identify data section")

    def test_identify_misc_section(self):
        self.assertEqual(identify_config_section("atmos_timestep"), "misc", "Failed to identify misc section")

    def test_invalid_field(self):
        field_to_update = "foo"
        with self.assertRaises(RuntimeError) as context:
            identify_config_section(field_to_update)
        self.assertEqual(str(context.exception), f"Unrecognised field: {field_to_update}")


class TestLogUpdate(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config["metadata"] = {"model_id": "updated"}
        self.config["ADDITIONAL INFO"] = {"updates": ""}

        self.field = "experiment_id"
        self.old_value = "old"
        self.new_value = "new"
        self.date = datetime.today().strftime('%Y-%m-%d')

        return self

    def test_log_first_update(self):
        log_update(self.config, self.field, self.old_value, self.new_value)
        expected_msg = (f'". {self.field.capitalize()} was updated from `{self.old_value}` to `{self.new_value}` '
                        f'({self.date})"')
        self.assertEqual(self.config["ADDITIONAL INFO"]["updates"], expected_msg,
                         f"Failed to correctly log first update message.")

    def test_log_additional_update(self):
        self.config["ADDITIONAL INFO"]["updates"] = ". Previous update"
        log_update(self.config, self.field, self.old_value, self.new_value)

        expected_msg = (f'". Previous update. {self.field.capitalize()} was updated from `{self.old_value}` to '
                        f'`{self.new_value}` ({self.date})"')
        self.assertEqual(self.config["ADDITIONAL INFO"]["updates"], expected_msg,
                         "Failed to correctly log additional update message")
