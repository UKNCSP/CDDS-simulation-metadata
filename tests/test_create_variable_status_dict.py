# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Tests scripts.create_variable_status_dict.py"""

import unittest

from scripts.create_variable_status_dict import get_all_models, get_variable_status
from scripts.common import read_json
from scripts.constants import MAPPINGS_FILE_LOCATION


class TestGetAllModels(unittest.TestCase):

    def test_get_all_models(self):
        mappings_dict = read_json(MAPPINGS_FILE_LOCATION)
        all_models = get_all_models(mappings_dict)
        expected = {'HadGEM3-GC5', 'UKESM1-3', 'HadGEM3-GC31', 'UKESM1', 'UKESM2'}
        self.assertEqual(get_all_models(mappings_dict), expected, f"Failed to identify all models in mappings:\nGot: "
                         f"{all_models}\nExpected: {expected}")


if __name__ == "__main__":
    unittest.main()
