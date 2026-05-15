# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Tests scripts.create_metadata_conf"""

import unittest

from scripts.create_metadata_conf import (set_calendar, normalise_datetime, process_metadata, check_for_missing_inputs,
                                          check_parent_fields, check_mass_data_class_attributes, check_datetime_fields,
                                          check_model_workflow_id, check_variant_labels, check_atmos_timestep,
                                          check_start_end_logic, check_fixed_fields, check_cvs, format_warning_message,
                                          create_filename, sort_to_categories)


class TestSetCalendar(unittest.TestCase):

    def test_set_calendar_success(self):
        for calendar in ("gregorian", "360_day"):
            self.assertEqual(set_calendar(calendar), {}, f"Failed to set calendar as {calendar}")

    def test_set_calendar_failure(self):
        expected = {'calendar': 'incompatible calendar: expected 360_day or gregorian/standard'}
        self.assertEqual(set_calendar("BAZINGA"), expected, "Failed to correctly flag an unrecognised calendar.")


class TestNormaliseDatetime(unittest.TestCase):

    def test_normalise_datetime_success(self):
        times = ("1900", "1900-01", "1900-01-01", "1900-01-01T00", "1900-01-01T00:00", "1900-01-01T00:00:00",
                 "1900-01-01T00:00:00Z")
        for datetime in times:
            normalised_datetime, errors = normalise_datetime(datetime, {}, "start_date")
            self.assertEqual(normalised_datetime, "1900-01-01T00:00:00Z", f"Failed to normalise datetime: {datetime}")
            self.assertEqual(errors, {}, f"Invalid datetime error has been triggered unexpectedly for a valid input")

    def test_normalise_datetime_failure(self):
        normalised_datetime, errors = normalise_datetime("1900-00-00T", {}, "start_date")
        err_msg = "Failed to trigger the expected error for an invalid datetime input"
        self.assertEqual(normalised_datetime, "1900-00-00T", "Failed to return an invalid datetime unaltered")
        self.assertEqual(errors, {'datetime': 'invalid datetime format for start_date'}, err_msg)


class TestProcessMetadata(unittest.TestCase):

    def test_process_metadata(self):
        match_list = [('Issue Type', 'New'), ('Model Workflow ID', 'u-dw874'), ('Activity ID (MIP)', 'CMIP'),
                      ('Experiment ID', 'piControl'), ('Model ID', 'UKCM2a-0-HH'), ('Variant label', 'r1i1p1f1'),
                      ('Start Date', '1850-01-01T00:00:00Z'), ('End Date', '2022-01-01T00:00:00Z'),
                      ('Base Date', '1850-01-01T00:00:00Z'), ('Branch Method', 'standard'),
                      ('Calendar Type', 'gregorian'), ('Institution ID', 'MOHC'), ('MIP Era', 'CMIP7'),
                      ('Atmospheric Timestep', '600'), ('Mass Data Class', 'crum'), ('Parent MIP Era', 'CMIP7'),
                      ('Child Branch Date', '1850-01-01T00:00:00Z'), ('Parent Branch Date', '1951-01-01T00:00:00Z'),
                      ('Parent Experiment ID', 'piControl-spinup'), ('Parent Activity ID (MIP)', 'CMIP'),
                      ('Parent Model ID', 'UKCM2a-0-HH'), ('Parent Time Units', 'days since 1850-01-01T00:00:00Z'),
                      ('Parent Variant Label', 'r1i1p1f1'), ('Mass Ensemble Member ID', '_No response_')]
        expected = {
            'issue_type': 'New',
            'base_date': '1850-01-01T00:00:00Z',
            'branch_method': 'standard',
            'branch_date_in_child': '1850-01-01T00:00:00Z',
            'branch_date_in_parent': '1951-01-01T00:00:00Z',
            'parent_experiment_id': 'piControl-spinup',
            'parent_mip': 'CMIP',
            'parent_mip_era': 'CMIP7',
            'parent_model_id': 'UKCM2a-0-HH',
            'parent_time_units': 'days since 1850-01-01T00:00:00Z',
            'parent_variant_label': 'r1i1p1f1',
            'calendar': 'gregorian',
            'experiment_id': 'piControl',
            'institution_id': 'MOHC',
            'mip': 'CMIP',
            'mip_era': 'CMIP7',
            'variant_label': 'r1i1p1f1',
            'model_id': 'UKCM2a-0-HH',
            'start_date': '1850-01-01T00:00:00Z',
            'end_date': '2022-01-01T00:00:00Z',
            'mass_data_class': 'crum',
            'mass_ensemble_member': '',
            'model_workflow_id': 'u-dw874',
            'atmos_timestep': '600'
        }
        err_msg = "Failed to reformat issue body into the expected dictionary format"
        self.assertEqual(process_metadata(match_list), expected, err_msg)


class TestChecks(unittest.TestCase):

    def setUp(self):
        self.metadata_dictionary = {
            'issue_type': 'New',
            'base_date': '1850-01-01T00:00:00Z',
            'branch_method': 'standard',
            'branch_date_in_child': '1850-01-01T00:00:00Z',
            'branch_date_in_parent': '1951-01-01T00:00:00Z',
            'parent_experiment_id': 'piControl-spinup',
            'parent_mip': 'CMIP',
            'parent_mip_era': 'CMIP7',
            'parent_model_id': 'UKCM2a-0-HH',
            'parent_time_units': 'days since 1850-01-01',
            'parent_variant_label': 'r1i1p1f1',
            'calendar': 'gregorian',
            'experiment_id': 'piControl',
            'institution_id': 'MOHC',
            'mip': 'CMIP',
            'mip_era': 'CMIP7',
            'variant_label': 'r1i1p1f1',
            'model_id': 'UKCM2a-0-HH',
            'start_date': '1850-01-01T00:00:00Z',
            'end_date': '2022-01-01T00:00:00Z',
            'mass_data_class': 'crum',
            'mass_ensemble_member': '',
            'model_workflow_id': 'u-dw874',
            'atmos_timestep': '600'
        }

        return self

    def test_check_missing_inputs(self):
        err_msg = "Incorrectly flagging missing fields where all required fields are present"
        self.assertEqual(check_for_missing_inputs(self.metadata_dictionary, {}), {}, err_msg)

        for key, _ in self.metadata_dictionary.items():
            self.metadata_dictionary[key] = ""
        errors = check_for_missing_inputs(self.metadata_dictionary, {})
        expected = {
            'missing_required_field': [
                'Missing field mass_data_class', 'Missing field branch_method', 'Missing field calendar',
                'Missing field variant_label', 'Missing field model_workflow_id', 'Missing field base_date',
                'Missing field experiment_id', 'Missing field model_id', 'Missing field institution_id',
                'Missing field atmos_timestep', 'Missing field end_date', 'Missing field start_date',
                'Missing field mip_era', 'Missing field mip'
            ]
        }
        self.assertCountEqual(errors, expected, f"Failed to flag all missing requried fields.")

    def test_check_parent_fields(self):
        # Check that all fields present under branch method standard passes
        err_msg = err_msg = "Incorrectly flagging missing parent fields where all required fields are present"
        self.assertEqual(check_parent_fields(self.metadata_dictionary, {}), {}, err_msg)

        # Check that all fields present under no parent flags unexpected parent fields
        self.metadata_dictionary["branch_method"] = "no parent"
        err_msg = "Failed to flag unexpected parent fields when branch method set to no parent."
        expected = {
            'unexpected_parent_field': [
                'unexpected field: parent_time_units', 'unexpected field: parent_mip',
                'unexpected field: parent_model_id', 'unexpected field: branch_date_in_child',
                'unexpected field: parent_variant_label', 'unexpected field: parent_experiment_id',
                'unexpected field: branch_date_in_parent', 'unexpected field: parent_mip_era'
            ]
        }
        self.assertCountEqual(check_parent_fields(self.metadata_dictionary, {}), expected, err_msg)

        # Check that no parent fields present under branch method no parent passes
        parent_fields = ('branch_date_in_child', 'branch_date_in_parent', 'parent_experiment_id', 'parent_mip',
                         'parent_mip_era', 'parent_model_id', 'parent_time_units', 'parent_variant_label')
        for field in parent_fields:
            self.metadata_dictionary[field] = ""
        err_msg = "Incorrectly flagging unexpected fields where parent fields are blank with branch method no parent"
        self.assertEqual(check_parent_fields(self.metadata_dictionary, {}), {}, err_msg)

        # Check that no parent fields present under branch method standard flags missing parent fields
        self.metadata_dictionary["branch_method"] = "standard"
        err_msg = "Failed to flag missing parent fields with branch method standard"
        expected = {
            'missing_parent_field': [
                'missing required parent field: parent_mip_era', 'missing required parent field: branch_date_in_parent',
                'missing required parent field: branch_date_in_child',
                'missing required parent field: parent_time_units', 'missing required parent field: parent_mip',
                'missing required parent field: parent_experiment_id', 'missing required parent field: parent_model_id',
                'missing required parent field: parent_variant_label'
            ]
        }
        self.assertCountEqual(check_parent_fields(self.metadata_dictionary, {}), expected, self.metadata_dictionary)

    def test_check_mass_data_class_attributes(self):
        err_msg = "Incorrectly flagging a valid mass_data_class and mass_ensemble_member input"
        self.assertEqual(check_mass_data_class_attributes(self.metadata_dictionary, {}), {}, err_msg)

        self.metadata_dictionary["mass_data_class"] = "ens"
        self.metadata_dictionary["mass_ensemble_member"] = "an_id"
        self.assertEqual(check_mass_data_class_attributes(self.metadata_dictionary, {}), {}, err_msg)

        self.metadata_dictionary["mass_ensemble_member"] = ""
        expected = {'missing_mass_field': 'missing field: mass_ensemble_member'}
        err_msg = "Failed to flag missing mass_ensemble_member when mass_data_class is 'ens'"
        self.assertEqual(check_mass_data_class_attributes(self.metadata_dictionary, {}), expected, err_msg)

        self.metadata_dictionary["mass_data_class"] = "crum"
        self.metadata_dictionary["mass_ensemble_member"] = "an_id"
        expected = {'unexpected_mass_field': 'unexpected field: mass_ensemble_member'}
        err_msg = "Failed to flag unexpected mass_ensemble_member when mass_data_class is 'crum'"
        self.assertEqual(check_mass_data_class_attributes(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_datetime_fields(self):
        self.metadata_dictionary["start_date"] = "1850-01-01"
        err_msg = "Failed to update normalised datetime fields"
        self.assertEqual(check_datetime_fields(self.metadata_dictionary, {}), {}, err_msg)

        self.metadata_dictionary["start_date"] = "not_a_date"
        err_msg = "Failed to flag an un normalised or invalid datetime input"
        expected = {'datetime': 'invalid datetime format for start_date'}
        self.assertEqual(check_datetime_fields(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_model_workflow_id(self):
        err_msg = "Incorrectly flagged a valid workflow id as invalid"
        for id in ("ab-cd123", "u-ab123"):
            self.metadata_dictionary["model_workflow_id"] = id
            self.assertEqual(check_model_workflow_id(self.metadata_dictionary, {}), {}, err_msg)

        self.metadata_dictionary["model_workflow_id"] = "not_an_id"
        expected = {'workflow_id_format': 'model workflow ID is incorrectly formatted: expected a-bc123 or ab-cd123'}
        err_msg = "Failed to flag an invalid model workflow ID"
        self.assertEqual(check_model_workflow_id(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_variant_labels(self):
        err_msg = "Incorrectly flagged a valid variant label as invalid"
        self.assertEqual(check_variant_labels(self.metadata_dictionary, {}), {}, err_msg)

        self.metadata_dictionary["variant_label"] = "not_a_label"
        self.metadata_dictionary["parent_variant_label"] = "still_not_a_label"
        err_msg = "Failed to flag an invalid variant label"
        expected = {
            'label_format': ('variant label or parent variant label is incorrectly formatted: expected r1i1p1f1 like '
                             'format')
        }
        self.assertEqual(check_variant_labels(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_atmos_timestep(self):
        err_msg = "Incorrectly flagged a valid atmospheric timestep as invalid"
        self.assertEqual(check_atmos_timestep(self.metadata_dictionary, {}), {}, err_msg)

        err_msg = "Failed to flag an invalid atmsopheric timestep"
        expected = {"timestep_logic": "atmospheric timestep is invalid"}
        for timestep in ("-250", "7.5"):
            self.metadata_dictionary["atmos_timestep"] = timestep
            self.assertEqual(check_atmos_timestep(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_start_end_logic(self):
        err_msg = "Incorrectly flagged a valid atmospheric timestep as invalid"
        self.assertEqual(check_start_end_logic(self.metadata_dictionary, {}), {}, err_msg)

        # Check that error is flagged if end date comes before start date
        self.metadata_dictionary["end_date"] = "1500-01-01T00:00:00Z"
        err_msg = "Failed to flag invalid datetime logic"
        expected = {"datetime_logic": "end date cannot be earlier than start date"}
        self.assertEqual(check_start_end_logic(self.metadata_dictionary, {}), expected, err_msg)

        # Check that error is flagged if check is unable to date place due to missing start or enddate
        self.metadata_dictionary["end_date"] = ""
        errors = {"datetime": "invalid datetime format for end_date"}
        err_msg = "Failed to flag inability to perform start end time logic check due to missing field"
        expected = {"datetime": "invalid datetime format for end_date"}

        self.assertEqual(check_start_end_logic(self.metadata_dictionary, errors), expected, err_msg)

    def test_check_fixed_fields_success(self):
        errors = check_fixed_fields(self.metadata_dictionary, {})
        err_msg = f"Incorrectly flagged a valid fixed field as invalid with error message '{errors}'"
        self.assertEqual(errors, {}, err_msg)

    def test_check_branch_method(self):
        self.metadata_dictionary["branch_method"] = "wrong"
        err_msg = "Failed to flag invalid branch_method"
        expected = {'unrecognised_input': ["branch_method must have the value 'no parent' or 'standard'"]}
        self.assertEqual(check_fixed_fields(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_model_id(self):
        self.metadata_dictionary["model_id"] = "wrong"
        err_msg = "Failed to flag invalid model_id"
        expected = {
            "unrecognised_input": [
                "model_id must have the value 'UKCM2-0-LL', 'UKCM2a-0-HH', 'UKESM1-3-LL' or 'HadGEM3-GC31-MM'",
                "parent_model_id must match model_id 'UKCM2a-0-HH'"
            ]
        }
        self.assertCountEqual(check_fixed_fields(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_fixed_fields_standard(self):
        self.metadata_dictionary["base_date"] = "wrong"
        self.metadata_dictionary["mass_data_class"] = "wrong"
        self.metadata_dictionary["mip_era"] = "wrong"
        self.metadata_dictionary["parent_mip_era"] = "wrong"
        self.metadata_dictionary["parent_model_id"] = "wrong"
        self.metadata_dictionary["parent_time_units"] = "wrong"
        err_msg = "Failed to flag invalid fixed field with branch method standard"
        expected = {
            'unrecognised_input': [
                "base date 'wrong' differs from the expected 1850-01-01T00:00:00Z. If you wish to use 'wrong', please "
                "contact a member of the CDDS team",
                "mip_era and parent_mip_era must have the value 'CMIP7'",
                "mip_era and parent_mip_era must have the value 'CMIP7'",
                "parent_model_id must match model_id 'UKCM2a-0-HH'",
                "parent_time_units must have the value 'days since 1850-01-01T00:00:00Z'",
                "mass_data_class must have the value 'ens' or 'crum'"
            ]
        }
        self.assertCountEqual(check_fixed_fields(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_cvs_success(self):
        errors = check_cvs(self.metadata_dictionary, {})
        err_msg = f"Incorrectly flagged a valid field as invalid against cvs with error message '{errors}'"
        self.assertEqual(errors, {}, err_msg)

    def test_check_experiment_against_cvs(self):
        self.metadata_dictionary["experiment_id"] = "not_an_experiment"
        err_msg = "Failed to flag experiment ID missing from cvs"
        expected = {"cv_error": ["experiment id 'not_an_experiment' could not be found in the cvs"]}
        self.assertEqual(check_cvs(self.metadata_dictionary, {}), expected, err_msg)

    def test_check_cvs_failure(self):
        self.metadata_dictionary["institution_id"] = "wrong"
        self.metadata_dictionary["mip"] = "wrong"
        self.metadata_dictionary["parent_experiment_id"] = "wrong"
        self.metadata_dictionary["parent_mip"] = "wrong"
        err_msg = "Failed to flag invalid field as missing from cvs"
        expected = {
            'cv_error': [
                "institution_id 'wrong' could not be found in the cvs",
                "mip 'wrong' does not match one of the expected values "
                "'['CMIP']' given in the cvs",
                "parent experiment id 'wrong' does not match one of the expected "
                "values '['piControl-spinup']' given in the cvs",
                "parent mip 'wrong' does not match one of the expected values "
                "'['CMIP']' given in the cvs"
            ]
        }
        self.assertEqual(check_cvs(self.metadata_dictionary, {}), expected, err_msg)


class TestFormatWarningMessage(unittest.TestCase):

    def test_format_warning_message(self):
        errors = {
            'missing_required_field': ['Missing field mass_data_class'],
            'unexpected_parent_field': ['unexpected field: parent_time_units', 'unexpected field: parent_mip'],
            'missing_mass_field': 'missing field: mass_ensemble_member',
            'datetime': 'invalid datetime format for start_date'
        }
        err_msg = "Failed to correctly convert erros dictionary into a formatted warnings string"
        expected = ("Missing required field warning: Missing field mass data class.\nUnexpected parent field warning: "
                    "unexpected field: parent time units.\nUnexpected parent field warning: unexpected field: parent "
                    "mip.\nMissing mass field warning: missing field: mass ensemble member.\nDatetime warning: invalid "
                    "datetime format for start date.")
        self.assertEqual(format_warning_message(errors), expected, err_msg)


class TestCreateFilename(unittest.TestCase):

    def test_create_filename(self):
        err_msg = "Failed to correctly generate config filename"

        crum_metadata_dictionary = {
            'mass_data_class': 'crum',
            'mass_ensemble_member': '',
            'model_workflow_id': 'u-dw874',
        }
        self.assertEqual(create_filename(crum_metadata_dictionary), "u-dw874.cfg", err_msg)

        ens_metadata_dictionary = {
            'mass_data_class': 'ens',
            'mass_ensemble_member': 'id',
            'model_workflow_id': 'u-dw874',
        }
        self.assertEqual(create_filename(ens_metadata_dictionary), "u-dw874-id.cfg", err_msg)


class testSortToCategories(unittest.TestCase):

    def setUp(self):
        self.metadata_dictionary = {
            'issue_type': 'New',
            'base_date': '1850-01-01T00:00:00Z',
            'branch_method': 'standard',
            'branch_date_in_child': '1850-01-01T00:00:00Z',
            'branch_date_in_parent': '1951-01-01T00:00:00Z',
            'parent_experiment_id': 'piControl-spinup',
            'parent_mip': 'CMIP',
            'parent_mip_era': 'CMIP7',
            'parent_model_id': 'UKCM2a-0-HH',
            'parent_time_units': 'days since 1850-01-01T00:00:00Z',
            'parent_variant_label': 'r1i1p1f1',
            'calendar': 'gregorian',
            'experiment_id': 'piControl',
            'institution_id': 'MOHC',
            'mip': 'CMIP',
            'mip_era': 'CMIP7',
            'variant_label': 'r1i1p1f1',
            'model_id': 'UKCM2a-0-HH',
            'start_date': '1850-01-01T00:00:00Z',
            'end_date': '2022-01-01T00:00:00Z',
            'mass_data_class': 'crum',
            'mass_ensemble_member': '',
            'model_workflow_id': 'u-dw874',
            'atmos_timestep': '600'
        }

        self.expected = {
            '[metadata]': {
                'base_date': '1850-01-01T00:00:00Z',
                'branch_method': 'standard',
                'branch_date_in_child': '1850-01-01T00:00:00Z',
                'branch_date_in_parent': '1951-01-01T00:00:00Z',
                'parent_experiment_id': 'piControl-spinup',
                'parent_mip': 'CMIP',
                'parent_mip_era': 'CMIP7',
                'parent_model_id': 'UKCM2a-0-HH',
                'parent_time_units': 'days since 1850-01-01T00:00:00Z',
                'parent_variant_label': 'r1i1p1f1',
                'calendar': 'gregorian',
                'experiment_id': 'piControl',
                'institution_id': 'MOHC',
                'mip': 'CMIP',
                'mip_era': 'CMIP7',
                'variant_label': 'r1i1p1f1',
                'model_id': 'UKCM2a-0-HH'
            },
            '[data]': {
                'start_date': '1850-01-01T00:00:00Z',
                'end_date': '2022-01-01T00:00:00Z',
                'mass_data_class': 'crum',
                'mass_ensemble_member': '',
                'model_workflow_id': 'u-dw874'
            },
            '[misc]': {
                'atmos_timestep': '600'
            }
        }

        return self

    def test_sort_to_categories(self):
        err_msg = "Failed to correctly sort the metadata dictionary into the appropriate categories"
        self.assertEqual(sort_to_categories(self.metadata_dictionary), self.expected, err_msg)
