# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest

from unittest.mock import mock_open, patch

from scripts.delete_metadata import get_variable_list_filename


class TestGetVariableListFilename(unittest.TestCase):
    def test_get_variable_list_filename(self):
        mock_config = "[metadata]\nexperiment_id = 1pctCO2\nmodel_id = UKCM2-0-LL"
        with patch("builtins.open", mock_open(read_data=mock_config)):
            result = get_variable_list_filename("mock_config.cfg", "a-bc123")
        expected = "a-bc123_1pctCO2_UKCM2-0-LL.txt"
        self.assertEqual(result, expected, "Failed to construct variable list filename from metadata")
