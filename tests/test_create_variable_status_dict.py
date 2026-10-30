# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import unittest

from scripts.common import read_json
from scripts.constants import MAPPINGS_FILE_LOCATION
from scripts.create_variable_status_dict import get_all_models, get_variable_status


# This test may fail on a mappings update if a new model begins to be included in mappings or a model is removed from
# the mappings.
class TestGetAllModels(unittest.TestCase):
    def test_get_all_modles(self):
        mappings = read_json(MAPPINGS_FILE_LOCATION)
        expected = set(["UKCM2", "UKESM1-3x", "UKESM2", "UKESM1-3", "UKESM1", "UKESM1-1", "HadGEM3-GC31"])
        self.assertEqual(get_all_models(mappings), expected, "Failed to identify all models within the mappings")


# This is hard to test in its current format since it checks the status of every variable in the mappings and these
# status' regularly change with mappings updates. A better method may be to check the status of a single variable and
# have this function under a loop to make this more testable.
class TestGetVariableStatus(unittest.TestCase):
    def test_get_variable_status(self):
        pass
