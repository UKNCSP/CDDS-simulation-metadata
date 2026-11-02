# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import unittest
import os
import configparser

from scripts.generate_request import (process_issue_form, identify_mip_convert_plugin, update_request, REQUEST_TEMPLATE,
                                      validate_request, write_request)


class TestProcessIssueForm(unittest.TestCase):
    def test_process_issue_form(self):
        os.environ = {
            'ISSUE_BODY': ('### Model Workflow ID\n\nu-eb840\n\n### Request Type\n\nStandard Met Office Request\n\n'
                           '### Streams\n\nap4\n\n### Package Name\n\nround-1')
        }
        result = process_issue_form()
        expected = {'model_workflow_id': 'u-eb840',
                    'request_type': 'Standard Met Office Request',
                    'streams': 'ap4',
                    'package_name': 'round-1'}
        self.assertEqual(result, expected, "Failed to process request creation issue form.")


class TestIdentifyMIPPlugin(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config["metadata"] = {}
        return self

    def test_identify_mip_convert_plugin_ukcm2(self):
        self.config["metadata"] = {"model_id": "UKCM2-0-LL"}
        result = identify_mip_convert_plugin(self.config["metadata"])
        self.assertEqual(result, "UKCM2", "Failed to correctly identify `ukcm2` plugin")

    def test_identify_mip_convert_plugin_ukcm2a(self):
        self.config["metadata"] = {"model_id": "UKCM2a-0-HH"}
        result = identify_mip_convert_plugin(self.config["metadata"])
        self.assertEqual(result, "UKCM2", "Failed to correctly identify `ukcm2` plugin")

    def test_identify_mip_convert_plugin_ukesm(self):
        self.config["metadata"] = {"model_id": "UKESM1-3-LL"}
        result = identify_mip_convert_plugin(self.config["metadata"])
        self.assertEqual(result, "UKESM1p3", "Failed to correctly identify `ukesm1p3` plugin")

    def test_identify_mip_convert_plugin_hadgem(self):
        self.config["metadata"] = {"model_id": "HadGEM3-GC31-MM"}
        result = identify_mip_convert_plugin(self.config["metadata"])
        self.assertEqual(result, "HadGEM3", "Failed to correctly identify `HadGEM3` plugin")

    def test_identify_mip_convert_plugin_unrecognised(self):
        self.config["metadata"] = {"model_id": "foo"}
        with self.assertRaises(RuntimeError):
            identify_mip_convert_plugin(self.config["metadata"])


class TestUpdateRequest(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config["metadata"] = {
            'base_date': '1850-01-01T00:00:00Z',
            'branch_date_in_child': '',
            'branch_date_in_parent': '',
            'branch_method': 'no parent',
            'calendar': '360_day',
            'experiment_id': '1pctCO2',
            'institution_id': 'UKNCSP',
            'mip': 'CMIP',
            'mip_era': 'CMIP7',
            'model_id': 'UKCM2-0-LL',
            'parent_experiment_id': '',
            'parent_mip': '',
            'parent_mip_era': '',
            'parent_model_id': '',
            'parent_time_units': '',
            'parent_variant_label': '',
            'variant_label': 'r1i1p1f1'
        }
        self.config["data"] = {
            'end_date': '2100',
            'mass_data_class': 'crum',
            'mass_ensemble_member': '',
            'model_workflow_id': 'a-bc123',
            'start_date': '1850'
        }
        self.config["misc"] = {
            'atmos_timestep': '1200'
        }

        self.issue_info = {
            'model_workflow_id': 'a-bc123',
            'request_type': 'Standard Met Office Request',
            'streams': 'ap4',
            'package_name': 'round-1'
        }

        return self

    def test_update_request(self):
        result = update_request(REQUEST_TEMPLATE, self.config, self.issue_info)
        expected = {
            'metadata': {
                'base_date': '1850-01-01T00:00:00Z',
                'branch_date_in_child': '',
                'branch_date_in_parent': '',
                'branch_method': 'no parent',
                'calendar': '360_day',
                'experiment_id': '1pctCO2',
                'institution_id': 'UKNCSP',
                'license': 'CC-BY-4.0',
                'mip': 'CMIP',
                'mip_era': 'CMIP7',
                'model_id': 'UKCM2-0-LL',
                'parent_experiment_id': '',
                'parent_mip': '',
                'parent_mip_era': '',
                'parent_model_id': '',
                'parent_time_units': '',
                'parent_variant_label': '',
                'variant_label': 'r1i1p1f1'},
            'common': {
                'external_plugin': '',
                'external_plugin_location': '',
                'log_level': 'INFO',
                'mip_table_dir': '$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.5-v1.0.2',
                'mode': 'strict',
                'package': 'round-1',
                'root_ancil_dir': '$CDDS_ETC/ancil/',
                'root_data_dir': '$CDDS_DATA/$USER/data',
                'root_hybrid_heights_dir': '$CDDS_ETC/vertical_coordinates/',
                'root_proc_dir': '$CDDS_DATA/$USER/proc',
                'root_replacement_coordinates_dir': '$CDDS_ETC/horizontal_coordinates/',
                'sites_file': '$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt',
                'standard_names_dir': '$CDDS_ETC/standard_names/',
                'standard_names_version': '93',
                'workflow_basename': 'UKCM2-0-LL_1pctCO2_r1i1p1f1_round-1'},
            'conversion': {
                'continue_if_mip_convert_failed': 'False',
                'cylc_args': '-v',
                'mip_convert_plugin': 'UKCM2',
                'skip_archive': 'False',
                'skip_configure': 'False',
                'skip_extract': 'False',
                'skip_extract_validation': 'False',
                'skip_qc': 'False'},
            'data': {
                'data_version': 'v20261102',
                'end_date': '2100',
                'mass_data_class': 'crum',
                'mass_ensemble_member': '',
                'model_workflow_id': 'a-bc123',
                'output_mass_root': 'moose:/adhoc/projects/cdds',
                'output_mass_suffix': 'production',
                'start_date': '1850',
                'streams': 'ap4',
                'variable_list_file': '<UPDATE_WITH_PATH>/variables/v1.2.2.5/a-bc123_1pctCO2_UKCM2-0-LL.txt'},
            'misc': {'atmos_timestep': '1200'},
            'netcdf_global_attributes': {
                'data_specs_version': 'MIP-DS7.1.0.0',
                'drs_specs': 'MIP-DRS7',
                'region': 'glb'}
        }
        self.assertEqual(result, expected, "Failed to update request from metadata config file.")


class TestValidateRequest(unittest.TestCase):
    def setUp(self):
        self.request = {
            'metadata': {
                'base_date': '1850-01-01T00:00:00Z',
                'branch_date_in_child': '',
                'branch_date_in_parent': '',
                'branch_method': 'standard',
                'calendar': '360_day',
                'experiment_id': '1pctCO2',
                'institution_id': 'UKNCSP',
                'license': 'CC-BY-4.0',
                'mip': 'CMIP',
                'mip_era': 'CMIP7',
                'model_id': 'UKCM2-0-LL',
                'parent_experiment_id': 'piControl',
                'parent_mip': 'CMIP',
                'parent_mip_era': 'CMIP7',
                'parent_model_id': 'UKCM2-0-LL',
                'parent_time_units': 'days since 1850-01-01',
                'parent_variant_label': 'r1i1p1f1',
                'variant_label': 'r1i1p1f1'},
            'common': {
                'external_plugin': '',
                'external_plugin_location': '',
                'log_level': 'INFO',
                'mip_table_dir': '$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.5-v1.0.2',
                'mode': 'strict',
                'package': 'round-1',
                'root_ancil_dir': '$CDDS_ETC/ancil/',
                'root_data_dir': '$CDDS_DATA/$USER/data',
                'root_hybrid_heights_dir': '$CDDS_ETC/vertical_coordinates/',
                'root_proc_dir': '$CDDS_DATA/$USER/proc',
                'root_replacement_coordinates_dir': '$CDDS_ETC/horizontal_coordinates/',
                'sites_file': '$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt',
                'standard_names_dir': '$CDDS_ETC/standard_names/',
                'standard_names_version': '93',
                'workflow_basename': 'UKCM2-0-LL_1pctCO2_r1i1p1f1_round-1'},
            'conversion': {
                'continue_if_mip_convert_failed': 'False',
                'cylc_args': '-v',
                'mip_convert_plugin': 'UKCM2',
                'skip_archive': 'False',
                'skip_configure': 'False',
                'skip_extract': 'False',
                'skip_extract_validation': 'False',
                'skip_qc': 'False'},
            'data': {
                'data_version': 'v20261102',
                'end_date': '2100',
                'mass_data_class': 'crum',
                'mass_ensemble_member': '',
                'model_workflow_id': 'a-bc123',
                'output_mass_root': 'moose:/adhoc/projects/cdds',
                'output_mass_suffix': 'production',
                'start_date': '1850',
                'streams': 'ap4',
                'variable_list_file': '<UPDATE_WITH_PATH>/variables/v1.2.2.5/a-bc123_1pctCO2_UKCM2-0-LL.txt'},
            'misc': {'atmos_timestep': '1200'},
            'netcdf_global_attributes': {
                'data_specs_version': 'MIP-DS7.1.0.0',
                'drs_specs': 'MIP-DRS7',
                'region': 'glb'}
        }
        return self

    def test_validate_request_success(self):
        self.assertEqual(validate_request(self.request), None, "Incorrectly flagged valid request as invalid")

    def test_validate_request_experiment_failure(self):
        # Tests for invalid institution, license and experiment id.
        self.request["metadata"]["institution_id"] = "foo"
        self.request["metadata"]["license"] = "bar"
        self.request["metadata"]["experiment_id"] = "baz"
        expected_err_msg = ("Unable to locate experiment id against cvs, unable to continue validation:\n"
                            "['institution_id could not be found in the cvs', 'license does not match one of the "
                            "expected values given in the cvs', 'experiment id could not be found in the cvs']")
        with self.assertRaises(RuntimeError) as context:
            validate_request(self.request)
        self.assertEqual(str(context.exception), expected_err_msg)

    def test_validate_request_mip_failure(self):
        # Tests for invalid mip on a no parent branching method
        self.request["metadata"]["mip"] = "foo"
        expected_err_msg = ("Unable to valdidate request file against cvs:\n['mip does not match one of the expected "
                            "values given in the cvs']")
        with self.assertRaises(RuntimeError) as context:
            validate_request(self.request)
        self.assertEqual(str(context.exception), expected_err_msg)

    def test_validate_request_no_parent_failure(self):
        # Tests for invalid parent branching information
        self.request["metadata"]["parent_experiment_id"] = "foo"
        self.request["metadata"]["parent_mip"] = "bar"
        expected_err_msg = ("Unable to valdidate request file against cvs:\n['parent experiment id does not match one "
                            "of the expected values given in the cvs', 'parent mip does not match one of the expected "
                            "values given in the cvs']")
        with self.assertRaises(RuntimeError) as context:
            validate_request(self.request)
        self.assertEqual(str(context.exception), expected_err_msg)


# This is difficult to unit test since the function has multiple utilities including file creation, these should be
# separated to make this more testable.
class TestWriteRequest(unittest.TestCase):
    def test_write_request(self):
        pass
