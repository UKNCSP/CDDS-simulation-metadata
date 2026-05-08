# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import requests
import json

from scripts.constants import MAPPINGS_FILE_LOCATION

link = "https://raw.githubusercontent.com/UKNCSP/CDDS-CMIP7-mappings/refs/heads/main/data/condensed_mappings.json"
new_mapping_dict = requests.get(link).json()

with open(MAPPINGS_FILE_LOCATION, "w") as f:
    json.dump(new_mapping_dict, f, indent=4)
