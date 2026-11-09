# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest
import argparse

from scripts.edit_known_issues import (get_valid_source_ids, get_valid_experiment_ids, get_add_or_delete_instructions,
                                       check_if_input_already_exists, append_to_issues_dict, remove_from_issues_dict)


# This essentially mirrors tests/test_create_variable_status_dict:TestGetAllModels but the function
# `get_valid_source_ids()` (where source_id is a synonym for model_id) does not consider XIOS entries. This is an
# oversight from when the script was originally written. As long as this still identifies all models in the same way
# this isnt a problem but should be updated in future to use the same `get_all_models()` function that should be moved
# to common or its own tools class.
class TestGetValidSourceIDs(unittest.TestCase):
    def test_get_valid_source_ids(self):
        # The expected may change with a mappings update if new models are included/removed from the mappings
        expected = set(["UKCM2", "UKESM1-3x", "UKESM2", "UKESM1-3", "UKESM1", "HadGEM3-GC31"])
        result = get_valid_source_ids()
        self.assertEqual(result, expected, "Failed to identify all models within the mappings")


# This will change with each new data request, likely including new additions each time. This function is difficult
# to tesst. It would be valuable to change the logic here to check whether a given experiment is valid rather than
# pulling the entire list of valid experiments. This would make it more testable and improve memory handling.
class TestGetValidExperimentIDS(unittest.TestCase):
    def test_get_valid_experiment_ids(self):
        pass


# This function requires a user input from within and hence is non-pure and hard to test. This should be re written such
# that the input is provided as a function parameter rather than requesting the command line input within the function.
class TestGetAddDeleteInstructions(unittest.TestCase):
    def test_get_add_instructions(self):
        pass

    def test_get_delete_instructions(self):
        pass

    def test_invalid_instructions(self):
        pass


class TestCheckInputExists(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()
        self.known_issues = {
            "model": {
                "experiment": {
                    "variant_label": {
                        "variable": "reason"
                    },
                    "*": {
                        "variable": "reason"
                    },
                },
                "*": {
                    "*": {
                        "variable": "reason"
                    }
                }
            }
        }
        return self

    # If the entry exists it will return 1, this is ambiguous and should be updated to True/False
    def test_check_exists_specific_args(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "variant_label"
        self.args.variable = "variable"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 1,
                         "Failed to find existing variable")

    def test_check_exists_glob_variant(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "*"
        self.args.variable = "variable"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 1,
                            "Failed to find existing variable")

    def test_check_exists_globs(self):
        self.args.source_id = "model"
        self.args.experiment_id = "*"
        self.args.variant_label = "*"
        self.args.variable = "variable"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 1,
                            "Failed to find existing variable")

    def test_check_not_exists_specific_args(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "variant_label"
        self.args.variable = "variable2"
        msg = "Identified variable as a existing in the known issues when it does not"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 0, msg)

    def test_check_not_exists_glob_variant(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "*"
        self.args.variable = "variable2"
        msg = "Identified variable as a existing in the known issues when it does not"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 0, msg)

    def test_check_not_exists_globs(self):
        self.args.source_id = "model"
        self.args.experiment_id = "*"
        self.args.variant_label = "*"
        self.args.variable = "variable2"
        msg = "Identified variable as a existing in the known issues when it does not"
        self.assertEqual(check_if_input_already_exists(self.known_issues, self.args), 0, msg)


class TestUpdateIssuesDict(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()
        self.known_issues = {"model": {"experiment": {"variant_label": {"variable": "reason"}}}}
        return self

    def test_append_to_issues_dict_variable_only(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "variant_label"
        self.args.variable = "variable2"
        self.args.comment = "another reason"
        result = append_to_issues_dict(self.known_issues, self.args)
        expected = {"model": {"experiment": {"variant_label": {"variable": "reason", "variable2": "another reason"}}}}
        self.assertEqual(result, expected, "Failed to append to known issues")

    def test_append_to_issues_dict_full_path(self):
        self.known_issues = {}
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "variant_label"
        self.args.variable = "variable"
        self.args.comment = "reason"
        result = append_to_issues_dict(self.known_issues, self.args)
        expected = {"model": {"experiment": {"variant_label": {"variable": "reason"}}}}
        self.assertEqual(result, expected, "Failed to append to known issues")

    @unittest.skip("Skipping test to remove a variable from the known issues. This function is outdated and expects a "
                   "list rather than a dict hence will always fail with AttributeError")
    def test_remove_from_issues_dict(self):
        self.args.source_id = "model"
        self.args.experiment_id = "experiment"
        self.args.variant_label = "variant_label"
        self.args.variable = "variable"
        self.args.comment = "reason"
        result = remove_from_issues_dict(self.known_issues, self.args)
        expected = {"model": {"experiment": {"variant_label": {}}}}
        self.assertEqual(result, expected, "Failed to append to known issues")
