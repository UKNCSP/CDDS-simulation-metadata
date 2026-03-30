# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Tests scripts.generate_request"""
import unittest
import configparser

from scripts.generate_request import (identify_mip_convert_plugin, update_template_with_metadata,
                                      update_template_with_data, update_template_with_misc, update_template_with_common,
                                      update_template_with_conversion, validate_request)


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


class TestUpdateTemplateWithMetadata(unittest.TestCase):

    def setUp(self):
        self.request = {
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
            }
        }

        config = configparser.ConfigParser()
        config['metadata'] = {
            "base_date": "1850-01-01T00:00:00Z",
            "branch_method": "standard",
            "branch_date_in_child": "1850-01-01T00:00:00Z",
            "branch_date_in_parent": "1850-01-01T00:00:00Z",
            "parent_experiment_id": "piControl",
            "parent_mip": "CMIP",
            "parent_mip_era": "CMIP7",
            "parent_model_id": "UKCM2-0-LL",
            "parent_time_units": "days since 1850-01-01T00:00:00Z",
            "parent_variant_label": "r1i1p1f1",
            "calendar": "gregorian",
            "experiment_id": "historical",
            "institution_id": "MOHC",
            "mip": "CMIP",
            "mip_era": "CMIP7",
            "variant_label": "r2i1p1f1",
            "model_id": "UKCM2-0-LL"
        }
        self.config = config

        self.expected = {
            'metadata': {
                'base_date': '1850-01-01T00:00:00Z',
                'branch_method': 'standard',
                'calendar': 'standard',
                'experiment_id': 'historical',
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
                'parent_time_units': 'days since 1850-01-01T00:00:00Z',
                'parent_variant_label': 'r1i1p1f1'
            }
        }
        return self

    def test_update_tempalte_with_metadata_gregorian(self):
        updated_request = update_template_with_metadata(self.request, self.config["metadata"])

        err_msg = "Failed to correctly populate metadata section of request with a gregorian calendar"
        self.assertEqual(updated_request, self.expected, err_msg)

    def test_update_template_with_metadata_360day(self):
        self.config["metadata"]["calendar"] = "360_day"
        updated_request = update_template_with_metadata(self.request, self.config["metadata"])
        self.expected["metadata"]["calendar"] = "360_day"
        err_msg = "Failed to correctly populate metadata section of request with a 360_day calendar"
        self.assertEqual(updated_request, self.expected, err_msg)


class TestUpdateTemplateWithData(unittest.TestCase):

    def setUp(self):
        self.request = {
            "data": {
                "end_date": "",
                "mass_data_class": "",
                "mass_ensemble_member": "",
                "model_workflow_id": "",
                "output_mass_suffix": "production",
                "output_mass_root": "moose:/adhoc/projects/cdds",
                "start_date": "",
                "streams": "ap4 ap5 ap6 ap7 ap8 ap9 apu apt inm onm ind ond",
                "variable_list_file": ""
            },
        }

        config = configparser.ConfigParser()
        config["metadata"] = {
            "experiment_id": "historical",
            "model_id": "UKCM2-0-LL"
        }
        config['data'] = {
            "start_date": "1850-01-01T00:00:00Z",
            "end_date": "2000-01-01T00:00:00Z",
            "mass_data_class": "crum",
            "mass_ensemble_member": "",
            "model_workflow_id": "u-dv623"
        }
        self.config = config

        self.expected = {
            'data': {
                'end_date': '2000-01-01T00:00:00Z',
                'mass_data_class': 'crum',
                'mass_ensemble_member': '',
                'model_workflow_id': 'u-dv623',
                'output_mass_suffix': 'production',
                'output_mass_root': 'moose:/adhoc/projects/cdds',
                'start_date': '1850-01-01T00:00:00Z',
                'streams': 'ap4 ap5 ap6 ap7 ap8 ap9 apu apt inm onm ind ond',
                'variable_list_file': 'variables/v1.2.2.3/u-dv623_historical_UKCM2-0-LL.txt'
            }
        }
        return self

    def test_update_template_with_data_crum(self):
        updated_request = update_template_with_data(self.request, self.config["data"], self.config["metadata"])
        err_msg = "Failed to populate data section of request file with mass data class 'crum'"
        self.assertEqual(updated_request, self.expected, err_msg)

    def test_update_template_with_data_ens(self):
        self.config["data"]["mass_data_class"] = "ens"
        self.config["data"]["mass_ensemble_member"] = "an_id"
        self.expected["data"]["mass_data_class"] = "ens"
        self.expected["data"]["mass_ensemble_member"] = "an_id"
        updated_request = update_template_with_data(self.request, self.config["data"], self.config["metadata"])
        err_msg = "Failed to populate data section of request file with mass data class 'ens'"
        self.assertEqual(updated_request, self.expected, err_msg)


class TestUpdateTemplateWithMisc(unittest.TestCase):

    def test_update_template_with_misc(self):
        self.request = {
            "misc": {
                "atmos_timestep": ""
            }
        }
        config = configparser.ConfigParser()
        config["misc"] = {
            "atmos_timestep": "1800"
        }
        self.config = config
        self.expected = {
            "misc": {
                "atmos_timestep": "1800"
            }
        }
        updated_request = update_template_with_misc(self.request, self.config["misc"])
        err_msg = "Failed to populate misc section of request file"
        self.assertEqual(updated_request, self.expected, err_msg)


class TestUpdateTemplateWithCommon(unittest.TestCase):

    def test_update_template_with_common(self):
        self.request = {
            "common": {
                "external_plugin": "",
                "external_plugin_location": "",
                "log_level": "INFO",
                "mip_table_dir": "$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.3-v1.0.2",
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
            }
        }
        config = configparser.ConfigParser()
        config["metadata"] = {
            "experiment_id": "historical",
            "model_id": "UKCM2-0-LL",
            "variant_label": "r2i1p1f1"
        }
        self.config = config
        self.expected = {
            'common': {
                'external_plugin': '',
                'external_plugin_location': '',
                'log_level': 'INFO',
                'mip_table_dir': '$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.3-v1.0.2',
                'mode': 'strict',
                'package': '',
                'root_ancil_dir': '$CDDS_ETC/ancil_testing/',
                'root_hybrid_heights_dir': '$CDDS_ETC/vertical_coordinates/',
                'root_replacement_coordinates_dir': '$CDDS_ETC/horizontal_coordinates/',
                'root_proc_dir': '$CDDS_DATA/proc',
                'root_data_dir': '$CDDS_DATA/data',
                'sites_file': '$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt',
                'standard_names_dir': '$CDDS_ETC/standard_names/',
                'standard_names_version': 'latest',
                'workflow_basename': 'UKCM2-0-LL_historical_r2i1p1f1'
            }
        }

        updated_request = update_template_with_common(self.request, self.config["metadata"])
        updated_request["common"]["package"] = ""
        err_msg = "Failed to populate common section of request file"
        self.assertEqual(updated_request, self.expected, err_msg)


class TestUpdateTemplateWithConversion(unittest.TestCase):

    def test_update_template_with_conversion(self):
        self.request = {
            "conversion": {
                "mip_convert_plugin": ""
            }
        }
        config = configparser.ConfigParser()
        config["metadata"] = {
            "model_id": "UKCM2-0-LL"
        }
        self.config = config
        self.expected = {
             "conversion": {
                "mip_convert_plugin": "UKCM2"
            }
        }

        updated_request = update_template_with_conversion(self.request, self.config["metadata"])
        err_msg = "Failed to populate conversion section of request file"
        self.assertEqual(updated_request, self.expected, err_msg)


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
