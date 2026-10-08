# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import metomi.isodatetime.parsers as parse
from metomi.isodatetime.data import Calendar

from configparser import ConfigParser

from constants import WORKFLOW_METADATA_DIR


class MetadataConfigTools:
    """A class for validate metadata files."""
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id

    def read_config(self):
        """Read a single config file from `workflow_metadata/*.cfg` for a given workflow."""
        self.config = ConfigParser()
        file_path = f"{WORKFLOW_METADATA_DIR}/{self.workflow_id}.cfg"
        self.config.read(file_path)
        if not self.config:
            raise FileNotFoundError(f"{file_path} does not exist.")

    def set_calendar(self):
        if self._calendar == "360_day":
            Calendar.default().set_mode(self._calendar)
        elif self._calendar == "proleptic_gregorian":
            Calendar.default().set_mode("gregorian")
        else:
            raise RuntimeError(f"Unrecognsied calednar: {self._calendar}")

    @property
    def _metadata_section(self):
        return self.config["metadata"]

    @property
    def _data_section(self):
        return self.config["data"]

    @property
    def _misc_section(self):
        return self.config["misc"]

    @property
    def _additional_info_section(self):
        return self.config["ADDITIONAL INFO"]

    @property
    def _model_id(self):
        return self._metadata_section["model_id"]

    @property
    def _experiment_id(self):
        return self._metadata_section["experiment_id"]

    @property
    def _variant_label(self):
        return self._metadata_section["variant_label"]

    @property
    def _calendar(self):
        return self._metadata_section["calendar"]

    @property
    def _run_length_years(self):
        """Returns the run length in years."""
        self.set_calendar()
        parser = parse.TimePointParser()
        start_date = parser.parse(self._data_section["start_date"])
        end_date = parser.parse(self._data_section["end_date"])
        run_length_days, _ = (end_date - start_date).get_days_and_seconds()

        return run_length_days / 365
