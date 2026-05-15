# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Tests scripts.generate_request"""
import unittest
import configparser

from scripts.generate_request import identify_mip_convert_plugin, update_request, validate_request
from scripts.constants import MIP_TABLE_DIR


class TestIdentifyPlugin(unittest.TestCase):

    def setUp(self):
        self.err_msg = "Unable to correctly identify plugin. Expected '{}', got '{}'"

        return self

    def test_identify_plugin_ukcm2(self):
        config = configparser.ConfigParser()
        config['metadata'] = {'model_id': 'UKCM2-0-LL'}

        plugin = identify_mip_convert_plugin(config["metadata"])
        expected = "UKCM2"
        self.assertEqual(plugin, expected, self.err_msg.format(expected, plugin))

    def test_identify_plugin_ukcma(self):
        config = configparser.ConfigParser()
        config['metadata'] = {'model_id': 'UKCM2a-0-HH'}

        plugin = identify_mip_convert_plugin(config["metadata"])
        expected = "UKCM2"
        self.assertEqual(plugin, expected, self.err_msg.format(expected, plugin))

    def test_identify_plugin_ukesm1p3(self):
        config = configparser.ConfigParser()
        config['metadata'] = {'model_id': 'UKESM1-3-LL'}

        plugin = identify_mip_convert_plugin(config["metadata"])
        expected = "UKESM1p3"
        self.assertEqual(plugin, expected, self.err_msg.format(expected, plugin))

    def test_identify_plugin_hadgem(self):
        config = configparser.ConfigParser()
        config['metadata'] = {'model_id': 'HadGEM3-GC31-MM'}

        plugin = identify_mip_convert_plugin(config["metadata"])
        expected = "HadGEM3"
        self.assertEqual(plugin, expected, self.err_msg.format(expected, plugin))

    def test_identify_plugin_failure(self):
        config = configparser.ConfigParser()
        config['metadata'] = {'model_id': 'bazinga'}

        self.assertRaises(RuntimeError, identify_mip_convert_plugin, config["metadata"])


class TestUpdateRequest(unittest.TestCase):

    def test_update_request(self):
        request = {
            "metadata": {
                "base_date": "",
                "branch_method": "",
                "calendar": "",
                "experiment_id": "",
                "institution_id": "",
                "license": "CC-BY-4.0",
                "mip": "",
                "mip_era": "",
                "model_id": "",
                "variant_label": "",
                "branch_date_in_child": "",
                "branch_date_in_parent": "",
                "parent_experiment_id": "",
                "parent_mip": "",
                "parent_mip_era": "",
                "parent_model_id": "",
                "parent_time_units": "",
                "parent_variant_label": "",
            },
            "netcdf_global_attributes": {
                "data_specs_version": "MIP-DS7.1.0.0",
                "drs_specs": "MIP-DRS7",
                "region": "glb"
            },
            "common": {
                "external_plugin": "",
                "external_plugin_location": "",
                "log_level": "INFO",
                "mip_table_dir": MIP_TABLE_DIR,
                "mode": "strict",
                "package": "",
                "root_ancil_dir": "$CDDS_ETC/ancil_testing/",
                "root_hybrid_heights_dir": "$CDDS_ETC/vertical_coordinates/",
                "root_replacement_coordinates_dir": "$CDDS_ETC/horizontal_coordinates/",
                "root_proc_dir": "$CDDS_DATA/proc",
                "root_data_dir": "$CDDS_DATA/data",
                "sites_file": "$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt",
                "standard_names_dir": "$CDDS_ETC/standard_names/",
                "standard_names_version": "latest",
                "workflow_basename": ""
            },
            "data": {
                "end_date": "",
                "mass_data_class": "",
                "mass_ensemble_member": "",
                "model_workflow_id": "",
                "output_mass_suffix": "production",
                "output_mass_root": "moose:/adhoc/projects/cdds",
                "start_date": "",
                "streams": "",
                "variable_list_file": ""
            },
            "misc": {
                "atmos_timestep": ""
            },
            "conversion": {
                "continue_if_mip_convert_failed": "False",
                "cylc_args": "-v",
                "mip_convert_plugin": "",
                "skip_extract": "False",
                "skip_extract_validation": "False",
                "skip_configure": "False",
                "skip_qc": "False",
                "skip_archive": "False"
            }
        }
        config = configparser.ConfigParser()
        config.read("tests/data/test_config.cfg")
        issue_info = {
            "model_workflow-id": "u-dv623",
            "streams": "ap4, ap5, ap6",
            "package_name": "test"
        }

        updated_request = update_request(request, config, issue_info)
        expected = {
            'metadata': {
                'base_date': '1850-01-01T00:00:00Z',
                'branch_method': 'standard',
                'calendar': 'standard',
                'experiment_id': '1pctCO2',
                'institution_id': 'MOHC',
                'license': 'CC-BY-4.0',
                'mip': 'CMIP',
                'mip_era': 'CMIP7',
                'model_id': 'UKCM2-0-LL',
                'variant_label': 'r2i1p1f1',
                'branch_date_in_child': '1850-01-01T00:00:00Z',
                'branch_date_in_parent': '1850-01-01T00:00:00Z',
                'parent_experiment_id': 'piControl',
                'parent_mip': 'CMIP',
                'parent_mip_era': 'CMIP7',
                'parent_model_id': 'UKCM2-0-LL',
                'parent_time_units': 'days since 1850-01-01',
                'parent_variant_label': 'r1i1p1f1'
            },
            'netcdf_global_attributes': {
                'data_specs_version': 'MIP-DS7.1.0.0',
                'drs_specs': 'MIP-DRS7',
                'region': 'glb'
            },
            'common': {
                'external_plugin': '',
                'external_plugin_location': '',
                'log_level': 'INFO',
                'mip_table_dir': MIP_TABLE_DIR,
                'mode': 'strict',
                'package': 'test',
                'root_ancil_dir': '$CDDS_ETC/ancil_testing/',
                'root_hybrid_heights_dir': '$CDDS_ETC/vertical_coordinates/',
                'root_replacement_coordinates_dir': '$CDDS_ETC/horizontal_coordinates/',
                'root_proc_dir': '$CDDS_DATA/proc',
                'root_data_dir': '$CDDS_DATA/data',
                'sites_file': '$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt',
                'standard_names_dir': '$CDDS_ETC/standard_names/',
                'standard_names_version': 'latest',
                'workflow_basename': 'UKCM2-0-LL_1pctCO2_r2i1p1f1'
            },
            'data': {
                'end_date': '2000-01-01T00:00:00Z',
                'mass_data_class': 'crum',
                'mass_ensemble_member': '',
                'model_workflow_id': 'u-dv623',
                'output_mass_suffix': 'production',
                'output_mass_root': 'moose:/adhoc/projects/cdds',
                'start_date': '1850-01-01T00:00:00Z',
                'streams': 'ap4 ap5 ap6',
                'variable_list_file': 'variables/v1.2.2.3/u-dv623_1pctCO2_UKCM2-0-LL.txt'
            },
            'misc': {
                'atmos_timestep': '1800'
            },
            'conversion': {
                'continue_if_mip_convert_failed': 'False',
                'cylc_args': '-v',
                'mip_convert_plugin': 'UKCM2',
                'skip_extract': 'False',
                'skip_extract_validation': 'False',
                'skip_configure': 'False',
                'skip_qc': 'False',
                'skip_archive': 'False'
            }
        }
        err_msg = f"Failed to update full request file.\nExpected:\n{expected}\nGot:\n{updated_request}"
        self.assertEqual(updated_request, expected, err_msg)


class TestValidateRequest(unittest.TestCase):

    def setUp(self):
        self.request = {
            "metadata": {
                "branch_method": "standard",
                "institution_id": "MOHC",
                "license": "CC-BY-4.0",
                "experiment_id": "historical",
                "parent_experiment_id": "piControl",
                "mip": "CMIP",
                "parent_mip": "CMIP"
            }
        }

        return self

    def test_success(self):
        self.assertEqual(None, validate_request(self.request), "validate_request ran into an unexpected RuntimeError")

    def test_bad_experiment_id(self):
        self.request["metadata"]["experiment_id"] = "an_invalid_experiment"
        with self.assertRaises(RuntimeError) as exc:
            outcome = validate_request(self.request)
        err_msg = ("Unable to locate experiment id against cvs, unable to continue validation:\n['experiment id could "
                   "not be found in the cvs']")
        self.assertEqual(str(exc.exception), err_msg)

    def test_complete_failure(self):
        bad_request = {
            "metadata": {
                "branch_method": "standard",
                "institution_id": "an_invalid_institution",
                "license": "an_invalid_license",
                "experiment_id": "historical",
                "parent_experiment_id": "wrong_parent_experiment",
                "mip": "not_a_mip",
                "parent_mip": "wrong_parent_mip"
            }
        }

        with self.assertRaises(RuntimeError) as exc:
            outcome = validate_request(bad_request)
        err_msg = ("Unable to valdidate request file against cvs:\n['institution_id could not be found in the cvs', "
                   "'license does not match one of the expected values given in the cvs', 'mip does not match one of "
                   "the expected values given in the cvs', 'parent experiment id does not match one of the expected "
                   "values given in the cvs', 'parent mip does not match one of the expected values given in the cvs']")
        self.assertEqual(str(exc.exception), err_msg)


if __name__ == "__main__":
    unittest.main()
