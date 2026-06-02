# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import requests
import json

from constants import MAPPINGS_FILE_LOCATION, MAPPING_FILE_VERSION

link = (f"https://raw.githubusercontent.com/UKNCSP/CDDS-CMIP7-mappings/refs/tags/{MAPPING_FILE_VERSION}/data/"
        "condensed_mappings.json")
new_mapping_dict = requests.get(link).json()

with open(MAPPINGS_FILE_LOCATION, "w") as f:
    json.dump(new_mapping_dict, f, indent=4)
