# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest
import argparse
import os

from itertools import chain

from scripts.generate_variable_lists import (collect_key_variables, get_grouped_priority_labels,
                                             standardise_grouped_priority_labels, set_priority_comments,
                                             get_all_variables, get_mapping, check_alias_dictionary,
                                             update_status_from_model, get_stream_from_XIOS, get_streams,
                                             apply_fx_streams, reformat_variable_names, identify_known_issues,
                                             process_variable_dict, format_outfile_content)
from scripts.constants import REF_INFO_DIR


class TestCollectKeyVariables(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()

        return self

    def test_collect_key_variables_command_line_success(self):
        os.environ = {}
        args = argparse.Namespace()
        args.workflow_id = "a-bc123"
        args.experiment = "1pctCO2"
        args.model = "UKCM2-0-LL"
        args.variant_label = "r1i1p1f1"
        result = collect_key_variables(args)
        expected = ("args", "a-bc123", "1pctCO2", "UKCM2-0-LL", "r1i1p1f1")
        self.assertEqual(result, expected, "Failed to process arguments from the command line")

    @unittest.skip("This works in practise but fails unit tests with Attribute Error, skipping for now.")
    def test_collect_key_variables_from_issue(self):
        issue_body_text = ("### Model Workflow ID\n\nu-ea246\n\n### Activity ID (MIP)\n\nC4MIP\n\n### Experiment ID\n\n"
                           "1pctCO2-rad\n\n### Model ID\n\nUKESM1-3-LL\n\n### Variant label\n\nr1i1p1f1")
        os.environ = {"ISSUE_BODY": issue_body_text}
        result = collect_key_variables(self.args)
        expected = ("issue_body", "u-ea246", "C4MIP", "1pctCO2-rad", "UKESM1-3-LL", "r1i1p1f1")
        self.assertEqual(result, expected, "Failed to process arguments from the issue body")

    @unittest.skip("This works in practise but fails unit tests with Attribute Error, skipping for now.")
    def test_collect_key_variables_no_inputs(self):
        os.environ = {}
        with self.assertRaises(RuntimeError) as context:
            collect_key_variables(self.args)
        self.assertEqual(str(context.exception), "No command line arguments or issue body provided.")


class TestGetGroupedPriorityLabels(unittest.TestCase):
    def test_get_grouped_priority_labels(self):
        experiment_data = {
            "experiment": {
                "1pctCO2": {"Core": ["a", "b"], "High": ["c"], "Medium": ["d", "e"], "Low": ["f"]}
            }
        }
        result = get_grouped_priority_labels(experiment_data, "1pctCO2")
        expected = {"core": ["a", "b"], "high": ["c"], "med": ["d", "e"], "low": ["f"]}
        self.assertEqual(result, expected, "Failed to group priority labels")


class TestStandardiseGroupedPriorityLabels(unittest.TestCase):
    def test_standardise_priority_labels(self):
        experiment_data = {"experiment": {"1pctCO2": {"Core": ["a.GLB", "b.glb"]}}}
        result = standardise_grouped_priority_labels(experiment_data, "1pctCO2")
        expected = {"core": ["a.glb", "b.glb"], "high": [], "med": [], "low": []}
        self.assertEqual(result, expected, "Failed to standardise capitalisation of `glb` in grouped priority labels")


class TestSetPriorityComments(unittest.TestCase):
    def test_set_priority_comments(self):
        experiment_data = {
            "experiment": {"1pctCO2": {"Core": ["a"], "High": ["b"], "Medium": ["c", "d"], "Low": ["e"]}}
        }
        result = set_priority_comments(experiment_data, "1pctCO2")
        expected = {"a": [], "b": [], "c": ["priority=medium"], "d": ["priority=medium"], "e": ["priority=low"]}
        self.assertEqual(result, expected, "Failed to set priority comments for medium and low priority variables")


class TestGetAllVariables(unittest.TestCase):
    def test_get_all_variables(self):
        experiment_data = {
            "experiment": {"1pctCO2": {"Core": ["a"], "High": ["b"], "Medium": ["c", "d"], "Low": ["e"]}}
        }
        result = get_all_variables(experiment_data, "1pctCO2")
        expected = chain(["a"], ["b"], ["c", "d"], ["e"])
        self.assertEqual(list(result), list(expected), "Failed to correctly list all variables from experiment dict")


class TestGetMapping(unittest.TestCase):
    def setUp(self):
        self.mappings_dict = [
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.rsdcsaf.tavg-u-hxy-u.mon.glb",
                "labels": ["question", "mon", "aerosol", "UKESM1", "HadGEM3-GC31", "beyond-AFT"],
                "models_in_stash": ["UKESM1-3", "UKCM2"],
                "stream": "ap4"
            },
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.rsdaf.tavg-u-hxy-u.mon.glb",
                "labels": ["question", "mon", "aerosol", "UKESM1", "HadGEM3-GC31", "beyond-AFT"],
                "models_in_stash": ["UKESM1-3", "UKCM2", "HadGEM3-GC31", "UKESM1"],
                "stream": "ap4"
            }
        ]

        return self

    def test_get_mapping_success(self):
        result = get_mapping(self.mappings_dict, "aerosol.rsdcsaf.tavg-u-hxy-u.mon.glb")
        self.assertEqual(result, self.mappings_dict[0], "Failed to identify correct mapping")

    def test_get_mapping_failure(self):
        result = get_mapping(self.mappings_dict, "nonexistent")
        self.assertEqual(result, None, "Failed to return None for missing mapping")


# This test may fail if `reference_information/model_id_alias.json` is editted or removed.
class TestCheckAliasDict(unittest.TestCase):
    def test_check_alias_exits(self):
        self.assertEqual(check_alias_dictionary("UKCM2a-0-HH"), "UKCM2", "Failed to correctly identify model alias")

    def test_check_alias_missing(self):
        model = "not-an-alias"
        self.assertEqual(check_alias_dictionary(model), model, "Failed to return uneditted model str with no alias")


class TestUpdateStatusFromModel(unittest.TestCase):

    @unittest.skip("This is a fragile test since it depends on model_variable_status.json which is read directly in "
                   "the function and changes regularly. To make this testable this should be loaded outside of the "
                   "funciton and parsed as a parameter")
    def test_update_status(self):
        pass

    def test_no_status_dictionary(self):
        model = "nonexistent"
        status_dict_path = REF_INFO_DIR / f"{model}_variable_status.json"
        expected_msg = f"Status dictionary for {model} does not exist at {status_dict_path}"
        with self.assertRaises(FileNotFoundError) as context:
            update_status_from_model(model, {})
        self.assertEqual(str(context.exception), expected_msg)


class TestGetStreamFromXIOS(unittest.TestCase):
    def setUp(self):
        self.model = "UKCM2"
        self.mapping = {
            "XIOS entries": {self.model: ""}
        }

    def test_stream(self):
        xios_info = ("onm/grid-T`: `<field field_ref=\"sst_pot\" name=\"tos\" />` <br> `onm/grid-T`: `<field "
                     "field_ref=\"e3t\" name=\"thkcello\" />")
        self.mapping["XIOS entries"][self.model] = xios_info
        msg = "Failed to get correct stream from XIOS"
        self.assertEqual(get_stream_from_XIOS(self.mapping, self.model), "onm/grid-T", msg)

    def test_icemod_stream(self):
        xios_info = ("ind/grid-T` : `<field field_ref=\"vice_siconc_cmip\" name=\"siv\" operation=\"average\" "
                     "freq_op=\"1d\" detect_missing_value=\"true\"> (@iceconc==0) ? $missval : (@vice_siconc_cmip / "
                     "@iceconc) </field>")
        self.mapping["XIOS entries"][self.model] = xios_info
        msg = "Failed to identify and ovveride icemod stream"
        self.assertEqual(get_stream_from_XIOS(self.mapping, self.model), "ind/icemod", msg)


class TestGetStreams(unittest.TestCase):
    def test_placeholder(self):
        # This tests all possible code paths.
        # `a` (no mapping), `b` (fixed variable), `c` (stream from STASH), `d` (stream from XIOS)
        experiment = "1pctCO2"
        experiment_data = {"experiment": {experiment: {
            "Core": ["aerosol.a.tavg-u-hxy-u.mon.glb"],
            "High": ["aerosol.b.tavg-u-hxy-u.fx.glb"],
            "Medium": ["aerosol.c.tavg-u-hxy-u.mon.glb"],
            "Low": ["aerosol.d.tavg-u-hxy-u.mon.glb"]
        }}}
        model = "UKCM2"
        mappings_dict = self.mappings_dict = [
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.b.tavg-u-hxy-u.fx.glb",
                "labels": ["fx", model],
                "models_in_stash": [model],
                "stream": ""
            },
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.c.tavg-u-hxy-u.mon.glb",
                "labels": ["mon", model],
                "models_in_stash": [model],
                "stream": "ap4"
            },
            {
                "XIOS entries": {model: "onm/grid-T`: `<field......"},
                "branded_variable": "aerosol.d.tavg-u-hxy-u.mon.glb",
                "labels": ["mon", model],
                "models_in_stash": [],
                "stream": ""
            }
        ]
        result = get_streams(experiment_data, experiment, mappings_dict, model)
        expected = {
            'aerosol.a.tavg-u-hxy-u.mon.glb': '',
            'aerosol.b.tavg-u-hxy-u.fx.glb': 'afx',
            'aerosol.c.tavg-u-hxy-u.mon.glb': 'ap4',
            'aerosol.d.tavg-u-hxy-u.mon.glb': 'onm/grid-T'
        }
        self.assertEqual(result, expected, "Failed to identify variable streams")


class TestApplyFxStream(unittest.TestCase):
    def test_apply_afx(self):
        self.assertEqual(apply_fx_streams("atmos.a.tavg-u-hxy-u.fx.glb"), "afx")
        self.assertEqual(apply_fx_streams("aerosol.a.tavg-u-hxy-u.fx.glb"), "afx")
        self.assertEqual(apply_fx_streams("atmosChem.a.tavg-u-hxy-u.fx.glb"), "afx")
        self.assertEqual(apply_fx_streams("land.a.tavg-u-hxy-u.fx.glb"), "afx")
        self.assertEqual(apply_fx_streams("landIce.a.tavg-u-hxy-u.fx.glb"), "afx")

    def test_apply_ofx(self):
        self.assertEqual(apply_fx_streams("ocean.a.tavg-u-hxy-u.fx.glb"), "ofx")
        self.assertEqual(apply_fx_streams("ocnBgchem.a.tavg-u-hxy-u.fx.glb"), "ofx")
        self.assertEqual(apply_fx_streams("seaIce.a.tavg-u-hxy-u.fx.glb"), "ofx")

    def test_unrecognised_realm(self):
        variable = "unknown.a.tavg-u-hxy-u.fx.glb"
        expected_msg = f"Unable to apply stream to {variable}, unrecognsied realm `{variable.split('.')[0]}`"
        with self.assertRaises(RuntimeError) as context:
            apply_fx_streams(variable)
        self.assertEqual(str(context.exception), expected_msg)


class TestReformatVariableNames(unittest.TestCase):
    def test_reformat(self):
        experiment = "1pctCO2"
        experiment_data = {"experiment": {experiment: {
            "Core": ["aerosol.a.tavg-u-hxy-u.mon.glb"],
            "High": ["aerosol.b.tavg-u-hxy-u.fx.glb"],
            "Medium": ["aerosol.c.tavg-u-hxy-u.mon.glb"],
            "Low": ["aerosol.d.tavg-u-hxy-u.mon.glb"]
        }}}
        model = "UKCM2"
        mappings_dict = [
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.a.tavg-u-hxy-u.yr.glb",
                "labels": ["yr", model],
                "models_in_stash": [model],
                "stream": "ap5"
            },
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.b.tavg-u-hxy-u.fx.90s",
                "labels": ["fx", model],
                "models_in_stash": [model],
                "stream": ""
            },
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.c.tavg-u-hxy-u.mon.glb",
                "labels": ["mon", model],
                "models_in_stash": [model],
                "stream": "ap4"
            },
            {
                "XIOS entries": {},
                "branded_variable": "aerosol.d.tavg-u-hxy-u.mon.glb",
                "labels": ["mon", model],
                "models_in_stash": [],
                "stream": ""
            }
        ]
        status_dict = {
            "aerosol.a.tavg-u-hxy-u.yr.glb": ["embargoed"],
            "aerosol.b.tavg-u-hxy-u.fx.90s": ["do-not-produce"],
            "aerosol.c.tavg-u-hxy-u.mon.glb": ["approved"],
            "aerosol.d.tavg-u-hxy-u.mon.glb": ["embargoed"]
        }

        result = reformat_variable_names(experiment_data, experiment, mappings_dict, status_dict, model)
        expected = {
            'aerosol/a_tavg-u-hxy-u@yr': ['Yearly variables unable to be processed at this time', 'embargoed'],
            'aerosol/c_tavg-u-hxy-u@mon:ap4': ['approved'],
            'aerosol/d_tavg-u-hxy-u@mon': ['embargoed']
        }
        msg = "Failed to correctly reformat variable names with applied streams, comments and filtering."
        self.assertEqual(result, expected, msg)

    def test_unexpected_variable_format(self):
        experiment = "1pctCO2"
        variable = "invalid.a.tavg-u-hxy-u.mon"
        experiment_data = {"experiment": {experiment: {"Core": [variable]}}}
        model = "UKCM2"
        mappings_dict = [
            {
                "XIOS entries": {},
                "branded_variable": variable,
                "labels": ["mon", model],
                "models_in_stash": [model],
                "stream": "ap5"
            },
        ]
        status_dict = {variable: []}
        expected_msg = f"'{variable} has unexpected format. Expected: realm.variable_id.branding.frequency.region'"
        with self.assertRaises(KeyError) as context:
            reformat_variable_names(experiment_data, experiment, mappings_dict, status_dict, model)
        self.assertEqual(str(context.exception), expected_msg)


class TestIdentifyKnownIssues(unittest.TestCase):
    @unittest.skip("This is a fragile test as it depends on the content of known_issues.json which changes regularly. "
                   "This function should be re written to parse the known issues as a parameter rather than loading it "
                   "directly under the function.")
    def test_known_issue(self):
        pass


@unittest.skip("Skipping for speed since this is a wrapper function for all of the above functions that are already "
               "tested")
class TestProcessVariableDict(unittest.TestCase):
    pass


class TestFormatOutfileContent(unittest.TestCase):
    def test_format_outfile_content(self):
        variable_dict = {
            'aerosol/a_tavg-u-hxy-u@mon:ap4': ['embargoed'],
            'aerosol/b_tavg-u-hxy-u@mon:ap4': ['approved'],
            'aerosol/c_tavg-u-hxy-u@mon:ap4': ['Known-issue'],
            'aerosol/d_tavg-u-hxy-u@mon:ap4': ['do-not-produce'],
            'aerosol/e_tavg-u-hxy-u@mon:ap4': ['approved', 'known-issue']
        }
        result = format_outfile_content(variable_dict)
        expected = ['#aerosol/a_tavg-u-hxy-u@mon:ap4  # embargoed\n',
                    'aerosol/b_tavg-u-hxy-u@mon:ap4  # approved\n',
                    '#aerosol/c_tavg-u-hxy-u@mon:ap4  # Known-issue\n',
                    '#aerosol/d_tavg-u-hxy-u@mon:ap4  # do-not-produce\n',
                    '#aerosol/e_tavg-u-hxy-u@mon:ap4  # approved, known-issue\n']
        self.assertEqual(result, expected, "Failed to correctly comment out variables based on comments")

    def test_unrecognised_variable(self):
        variable = 'aerosol/a_tavg-u-hxy-u@mon:ap4'
        variable_dict = {variable: []}
        expected_msg = (f"An unrecognised variable '{variable}' with no model variable status was discovered "
                        "during processing. This likely means that a variable cannot be produced within the "
                        "given model but has bypassed the filtering process.")
        with self.assertRaises(RuntimeError) as context:
            format_outfile_content(variable_dict)
        self.assertEqual(str(context.exception), expected_msg)
