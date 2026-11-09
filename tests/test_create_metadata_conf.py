# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest

from scripts.create_metadata_conf import set_calendar, create_filename, sort_to_categories


class TestSetCalendar(unittest.TestCase):
    def test_set_calendar_success(self):
        for calendar in ("360_day", "proleptic_gregorian"):
            self.assertEqual(set_calendar(calendar), {}, f"Failed to set calendar {calendar}")

    def test_set_calendar_failure(self):
        calendar = "foo"
        result = set_calendar(calendar)
        expected = {"calendar": "incompatible calendar: expected 360_day or proleptic_gregorian"}
        self.assertEqual(result, expected, f"Failed to warn of incompatible calendar: {calendar}")


class TestCreateFilename(unittest.TestCase):
    def test_create_filename_no_ensemble(self):
        meta_dict = {
            "model_workflow_id": "a-bc123",
            "mass_data_class": "crum",
            "mass_ensemble_member": ""
        }
        filename = create_filename(meta_dict)
        self.assertEqual(filename, "a-bc123.cfg")

    def test_create_filename_ensemble_member(self):
        meta_dict = {
            "model_workflow_id": "a-bc123",
            "mass_data_class": "ens",
            "mass_ensemble_member": "ens_id"
        }
        filename = create_filename(meta_dict)
        self.assertEqual(filename, "a-bc123-ens_id.cfg")


class TestSortToCategories(unittest.TestCase):
    def test_sort_to_categories(self):
        meta_dict = {
            "base_date": "1850-01-01T00:00:00Z",
            "branch_method": "no parent",
            "branch_date_in_child": "",
            "branch_date_in_parent": "",
            "parent_experiment_id": "",
            "parent_mip": "",
            "parent_mip_era": "",
            "parent_model_id": "",
            "parent_time_units": "",
            "parent_variant_label": "",
            "calendar": "360_day",
            "experiment_id": "1pctCO2",
            "institution_id": "UKNCSP",
            "mip": "CMIP",
            "mip_era": "CMIP7",
            "variant_label": "r1i1p1f1",
            "model_id": "UKCM2-0-LL",
            "start_date": "1850",
            "end_date": "2100",
            "mass_data_class": "crum",
            "mass_ensemble_member": "",
            "model_workflow_id": "a-bc123",
            "atmos_timestep": "1200"
        }
        organised_metadata = sort_to_categories(meta_dict)
        expected = {
            'ADDITIONAL INFO': {'notes': None, 'updates': ''},
            'data': {'end_date': '2100',
                    'mass_data_class': 'crum',
                    'mass_ensemble_member': '',
                    'model_workflow_id': 'a-bc123',
                    'start_date': '1850'},
            'metadata': {'base_date': '1850-01-01T00:00:00Z',
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
                        'variant_label': 'r1i1p1f1'},
            'misc': {'atmos_timestep': '1200'}
        }
        self.assertEqual(organised_metadata, expected, "Failed to sort metadata into the appropriate categories")
