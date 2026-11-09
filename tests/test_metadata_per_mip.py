# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest
import configparser

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import mock_open, patch

from scripts.metadata_per_mip import (glob_directory, update_workflow_info_for_mip, check_for_request, read_doc,
                                      restruct_dict_to_table)


class TestGlobDirectory(unittest.TestCase):
    def test_glob(self):
        file_suffix = ".cfg"
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            files = [f"a{file_suffix}", f"b{file_suffix}", f"c{file_suffix}"]
            for name in files:
                (directory / name).touch()
            result = glob_directory(directory, file_suffix)
            expected = [directory / f for f in files]
            self.assertEqual(result, expected, "Failed to glob all files in directory")

    def test_glob_no_files(self):
        file_suffix = ".cfg"
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            result = glob_directory(directory, file_suffix)
            self.assertEqual(result, [], "Failed to identify empty directory")


class TestUpdateWorkflowInfo(unittest.TestCase):
    def setUp(self):
        self.metadata_config = configparser.ConfigParser()
        self.metadata_config.read_dict({
            "metadata": {
                "mip": "CMIP",
                "model_id": "UKCM2-0-LL",
                "experiment_id": "1pctCO2",
                "variant_label": "r1i1p1f1",
            },
            "data": {"model_workflow_id": "u-ab123"},
        })

        return self

    def test_update_info_processing_true(self):
        mips_dict = {}
        with patch("scripts.metadata_per_mip.check_for_request", return_value=True):
            update_workflow_info_for_mip(self.metadata_config, mips_dict)
        expected = {
            'cmip': ['| UKCM2-0-LL 1pctCO2 r1i1p1f1 | '
                     '[u-ab123](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/'
                     'workflow_metadata/u-ab123.cfg) '
                     '| ✅ |\n']
        }
        self.assertEqual(mips_dict, expected, "Failed to update mip info for workflow in processing")

    def test_update_info_processing_false(self):
        mips_dict = {}
        with patch("scripts.metadata_per_mip.check_for_request", return_value=False):
            update_workflow_info_for_mip(self.metadata_config, mips_dict)
        expected = {
            'cmip': ['| UKCM2-0-LL 1pctCO2 r1i1p1f1 | '
                     '[u-ab123](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/'
                     'workflow_metadata/u-ab123.cfg) '
                     '| ❌ |\n']
        }
        self.assertEqual(mips_dict, expected, "Failed to update mip info for workflow in processing")


@unittest.skip("Skipping: function depends on evolving directory`workflow_metadata/`.")
class TestCheckForRequest(unittest.TestCase):
    # This funciton is hard to unit test since it uses a directory glob of workflow_metadata/ changes to this directory
    # may cause test failure. This function should be re written to take "all_requests" as a function parameter rather
    # than it being defined as part of the function.
    def test_request_exists(self):
        pass

    def test_request_not_exists(self):
        pass


class TestReadDoc(unittest.TestCase):
    def test_read_doc(self):
        doc = Path("example.md")
        file_content = "# Heading\nFirst line\nSecond line\n"
        with patch("builtins.open", mock_open(read_data=file_content)):
            result = read_doc(doc)
        expected = ["# Heading\n", "First line\n", "Second line\n"]
        self.assertEqual(result, expected, "Failed to correctly read existing doc file.")


class TestRestructDictToTable(unittest.TestCase):
    def test_restruct_dict_to_table(self):
        workflow_mips_dict = {"CMIP": ["simulation", "workflow_id", "processing_tag"]}
        result = restruct_dict_to_table(workflow_mips_dict, "CMIP")
        expected = ['\n', '| Simulation | Model Workflow ID | In Processing? |\n', '| ----- | ----- | ----- |\n',
                    'processing_tag', 'simulation', 'workflow_id']
        self.assertEqual(result, expected, "Failed to re structure mip information into markdown table.")
