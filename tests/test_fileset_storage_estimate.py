# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest

from scripts.fileset_storage_estimate import calc_size_estimate, check_for_hand_edits
from scripts.metadata_config_tools import MetadataConfigTools


class TestCalcSizeEstimate(unittest.TestCase):
    def test_calc_estimate_ukcm2(self):
        workflow = "u-dv623"   # Any changes to the workflow metadata config may result in test failure
        metadata = MetadataConfigTools(workflow)
        metadata_config = metadata.read_config()
        result = calc_size_estimate(metadata_config)
        self.assertEqual(result, 3.6, f"Failed to calculate size estimate for {workflow}")

    def test_calc_estimate_ukcm2a(self):
        workflow = "u-dy392"   # Any changes to the workflow metadata config may result in test failure
        metadata = MetadataConfigTools(workflow)
        metadata_config = metadata.read_config()
        result = calc_size_estimate(metadata_config)
        self.assertEqual(result, 42.0, f"Failed to calculate size estimate for {workflow}")

    def test_calc_estimate_ukesm1p3(self):
        workflow = "u-ec066"   # Any changes to the workflow metadata config may result in test failure
        metadata = MetadataConfigTools(workflow)
        metadata_config = metadata.read_config()
        result = calc_size_estimate(metadata_config)
        self.assertEqual(result, 3.1, f"Failed to calculate size estimate for {workflow}")

    def test_calc_estimate_override(self):
        workflow = "u-dx125"   # Any changes to the workflow metadata config may result in test failure
        metadata = MetadataConfigTools(workflow)
        metadata_config = metadata.read_config()
        result = calc_size_estimate(metadata_config)
        self.assertEqual(result, 240.2, f"Failed to calculate size estimate for {workflow}")


class TestCheckHandEdits(unittest.TestCase):
    def setUp(self):
        self.hand_edits = ["MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/mon 55.0",
                           "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/day 35.0",
                           "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/mon 48.0",
                           "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/day 32.0"]
        return self

    def test_hand_edits(self):
        path = "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical"
        self.assertEqual(check_for_hand_edits(self.hand_edits, path), True, "Failed to identify path with hand edits.")

    def test_no_hand_edits(self):
        path = "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKESM1-3-LL/1pctCO2"
        self.assertEqual(check_for_hand_edits(self.hand_edits, path), False, "Incorrectly flagged path as a hand edit")
