# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import unittest
import tempfile
import configparser

from scripts.update_all_variable_lists import extract_key_workflow_information


class TestExtractKeyWorkflowInformation(unittest.TestCase):
    def test_extract(self):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as file:
            file.write(
                "[metadata]\n"
                "experiment_id = experiment\n"
                "model_id = model\n"
                "variant_label = variant\n"
                "[data]\n"
                "model_workflow_id = workflow"
            )
            file.flush()
            result = extract_key_workflow_information(file.name)

        expected = {
            "experiment_id": "experiment",
            "model_id": "model",
            "variant_label": "variant",
            "workflow_id": "workflow"
        }
        self.assertEqual(result, expected, "Failed to extarct key information from workflow metadata config file")
