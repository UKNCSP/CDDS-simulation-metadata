# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import os
import requests
import json

from constants import MAPPINGS_FILE_LOCATION, DR_VERSION

README_TEMPLATE = """
<!--(C) British Crown Copyright 2025-2026, Met Office. Please see LICENSE.md for license details.--> 
# CDDS Simulation Metadata For CMIP7
[![Deploy static content to Pages]({})]({})

CURRENT MAPPINGS FILE VERSION: {}
CURRENT DATA REQUEST VERSION: {}

This CDDS simulation metadata repository is designed to process and store CMIP7 workflow metadata. If you have a new
 workflow that you wish to register, please fill out the issue form marked 'Add/Modify Workflow Metadata'. Upon form
 completion, you will receive a notification from our GitHub actions bot confirming your submission. If you wish to
 view the workflow metadata currently stored in the database, you can do so here: [CMIP7 Workflow Metadata]
(https://ukncsp.github.io/CDDS-simulation-metadata/ "A link to our GitHub pages"). Note that this table consists of
 only key metadata: to view the full metadata, click the link shown on the model workflow ID of interest.

Please note that any new additions may take up to an hour to become available to view and search on
 [CMIP7 Workflow Metadata](https://ukncsp.github.io/CDDS-simulation-metadata/ "A link to our GitHub pages").

If you make an error on your issue form, please edit the issue body with your changes or submit a new form containing
 the correct information. This will create a pull request that will be reviewed by a member of our team. It would be
 valuable to us if a brief comment could be left on the pull request explaining the reason for the change.
 For additional user guidance please see the wiki.
"""

mapping_file_version = os.environ['GH_ACTION_INPUT']
mapping_link = (f"https://raw.githubusercontent.com/UKNCSP/CDDS-CMIP7-mappings/refs/tags/{mapping_file_version}/data/"
        "condensed_mappings.json")
new_mapping_dict = requests.get(mapping_link).json()

with open(MAPPINGS_FILE_LOCATION, "w") as f:
    json.dump(new_mapping_dict, f, indent=4)

badge_link = "https://github.com/UKNCSP/CDDS-simulation-metadata/actions/workflows/deploy_pages.yml/badge.svg"
workflow_link = "https://github.com/UKNCSP/CDDS-simulation-metadata/actions/workflows/deploy_pages.yml"
with open("README.md", "w") as f:
    f.write(README_TEMPLATE.format(badge_link, workflow_link, mapping_file_version, DR_VERSION))
