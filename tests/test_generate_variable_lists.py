# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Tests scripts.generate_variable_lists.py"""

import unittest

from scripts.generate_variable_lists import (get_grouped_priority_labels, standardise_grouped_priority_labels,
                                             set_priority_comments, get_all_variables, get_mapping,
                                             check_alias_dictionary, update_status_from_model,
                                             modify_inm_onm_substreams, get_stream_from_XIOS, get_streams,
                                             reformat_variable_names, identify_known_issues, format_outfile_content)


class TestPriorityLabelOperations(unittest.TestCase):

    def setUp(self):
        self.minimal_data_request = {
            "experiment": {
                "1pctCO2": {
                    "Core": [
                        "atmos.areacella.ti-u-hxy-u.fx.GLB",
                        "atmos.cl.tavg-al-hxy-u.mon.GLB"
                    ],
                    "High": [
                        "aerosol.abs550aer.tavg-u-hxy-u.mon.glb",
                    ],
                    "Medium": [
                        "atmos.hur.tavg-700hPa-hxy-air.day.GLB",
                        "atmos.hur.tpt-100hPa-hxy-u.6hr.glb"
                    ],
                    "Low": []
                }
            }
        }

        self.grouped_labels = {
            "core": [
                "atmos.areacella.ti-u-hxy-u.fx.GLB",
                "atmos.cl.tavg-al-hxy-u.mon.GLB"
            ],
            "high": [
                "aerosol.abs550aer.tavg-u-hxy-u.mon.glb",
            ],
            "med": [
                "atmos.hur.tavg-700hPa-hxy-air.day.GLB",
                "atmos.hur.tpt-100hPa-hxy-u.6hr.glb"
            ],
            "low": []
        }

        self.standardised_grouped_labels = {
            "core": [
                "atmos.areacella.ti-u-hxy-u.fx.glb",
                "atmos.cl.tavg-al-hxy-u.mon.glb"
            ],
            "high": [
                "aerosol.abs550aer.tavg-u-hxy-u.mon.glb",
            ],
            "med": [
                "atmos.hur.tavg-700hPa-hxy-air.day.glb",
                "atmos.hur.tpt-100hPa-hxy-u.6hr.glb"
            ],
            "low": []
        }

        self.priority_comments = {
            'atmos.areacella.ti-u-hxy-u.fx.glb': [],
            'atmos.cl.tavg-al-hxy-u.mon.glb': [],
            'aerosol.abs550aer.tavg-u-hxy-u.mon.glb': [],
            'atmos.hur.tavg-700hPa-hxy-air.day.glb': ['priority=medium'],
            'atmos.hur.tpt-100hPa-hxy-u.6hr.glb': ['priority=medium']
        }

        return self

    def test_get_grouped_priority_labels(self):
        output = get_grouped_priority_labels(self.minimal_data_request, "1pctCO2")
        msg = f"Failed to correctly group variables by priority:\nGot: {output}\nExpected: {self.grouped_labels}"

        self.assertEqual(output, self.grouped_labels, msg)

    def test_standardise_grouped_priority_labels(self):
        output = standardise_grouped_priority_labels(self.minimal_data_request, "1pctCO2")
        msg = f"Failed to standardised grouped variables:\nGot: {output}\nExpected: {self.standardised_grouped_labels}"

        self.assertEqual(output, self.standardised_grouped_labels, msg)

    def test_set_priority_comments(self):
        output = set_priority_comments(self.minimal_data_request, "1pctCO2")
        msg = f"Failed to set variables priority comments:\nGot: {output}\nExpected: {self.priority_comments}"

        self.assertEqual(output, self.priority_comments, msg)


class TestGetAllVariables(unittest.TestCase):

    def test_get_all_variables(self):
        experiment_dict = {
            "experiment": {
                "1pctCO2": {
                    "Core": [
                        "atmos.areacella.ti-u-hxy-u.fx.GLB",
                        "atmos.cl.tavg-al-hxy-u.mon.GLB"
                    ],
                    "High": [
                        "aerosol.abs550aer.tavg-u-hxy-u.mon.glb",
                    ],
                    "Medium": [
                        "atmos.hur.tavg-700hPa-hxy-air.day.GLB",
                        "atmos.hur.tpt-100hPa-hxy-u.6hr.glb"
                    ],
                    "Low": []
                }
            }
        }
        output = list(get_all_variables(experiment_dict, "1pctCO2"))
        expected = ['atmos.areacella.ti-u-hxy-u.fx.glb', 'atmos.cl.tavg-al-hxy-u.mon.glb',
                    'aerosol.abs550aer.tavg-u-hxy-u.mon.glb', 'atmos.hur.tavg-700hPa-hxy-air.day.glb',
                    'atmos.hur.tpt-100hPa-hxy-u.6hr.glb']
        msg = f"Failed to list all variables for a given experiment:\nGot: {output}\nExpected: {expected}"

        self.assertEqual(output, expected, msg)


class TestGetMapping(unittest.TestCase):

    def setUp(self):
        self.mappings_dict = [
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.emidust.tavg-u-hxy-u.mon.glb",
                "labels": ["mon", "aerosol", "CMIP6", "UKESM1", "HadGEM3-GC31", "approved",
                           "diagnostic_review_data_available"],
                "models_in_stash": ["UKESM1-3", "HadGEM3-GC5", "HadGEM3-GC31", "UKESM1"],
                "stream": "ap4"
            },
            {
                "XIOS entries": {
                    "HadGEM3-GC5": ("onm/grid-T`: `<field field_ref=\"sst_pot\" name=\"tos\" />` <br> `onm/grid-T`:"
                    "`<field field_ref=\"e3t\" name=\"thkcello\" />")
                },
                "branded_variable": "ocean.tos.tavg-u-hm-sea.mon.glb",
                "labels": ["mon", "ocean", "CMIP6", "UKESM1", "HadGEM3-GC31", "approved"],
                "models_in_stash": [],
                "stream": ""
            }
        ]

        return self

    def test_get_mapping(self):
        output = get_mapping(self.mappings_dict, "aerosol.emidust.tavg-u-hxy-u.mon.glb")
        expected = {
            "XIOS entries": {},
            "branded_variable": "aerosol.emidust.tavg-u-hxy-u.mon.glb",
            "labels": ["mon", "aerosol", "CMIP6", "UKESM1", "HadGEM3-GC31", "approved",
                        "diagnostic_review_data_available"],
            "models_in_stash": ["UKESM1-3", "HadGEM3-GC5", "HadGEM3-GC31", "UKESM1"],
            "stream": "ap4"
        }
        msg = f"Failed identify mapping:\nGot: {output}\nExpected: {expected}"

        self.assertEqual(output, expected, msg)


class TestCheckAliasDictionary(unittest.TestCase):

    def test_check_alias_dictionary(self):
        output = check_alias_dictionary("UKCM2-0-LL")
        expected = "HadGEM3-GC5"
        msg = f"Failed to identify model alias:\nGot: {output}\nExpected: {expected}"

        self.assertEqual(output, expected, msg)


if __name__ == "__main__":
    unittest.main()
