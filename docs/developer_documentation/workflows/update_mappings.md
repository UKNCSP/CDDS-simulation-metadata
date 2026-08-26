<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [update_mappings.yml](../../../.github/workflows/update_mappings.yml)

## Overview

This workflow is triggered by workflow dispatch only and requires an input. **This workflow should only be run by CDDS team members**. The input should align with a tagged version of the [CDDS-CMIP7-mappings](https://github.com/UKNCSP/CDDS-CMIP7-mappings) repository. The workflow triggers [update_mapping_file.py](../../../scripts/update_mapping_file.py) which then uses the requests module to pull the [condesned_mappings.json](https://github.com/UKNCSP/CDDS-CMIP7-mappings/blob/main/data/condensed_mappings.json) from the given tagged version of[CDDS-CMIP7-mappings](https://github.com/UKNCSP/CDDS-CMIP7-mappings) and saves it as [mappings.json](../../../reference_information/mappings.json). This pulls in changes to variable labels, streams, STASH and XIOS which are utilised by many of the scripts in this repository. 

Once the new mappings file is present, the workflow will then run [create_variable_status_dict.py](../../../scripts/create_variable_status_dict.py) to update the approval status of each variable under each model. It will also run [update_all_variable_lists.py](../../../scripts/update_all_variable_lists.py) to propagate those changes through to the latest version of the variable lists (i.e. varaibles that have been approved since the last mappings update will be uncommented, new varaibles added to the [known_issues.json](../../../reference_information/known_issues.json) will be commented out along with any variables that are no longer approved.)

Each of the updated files are then automatically commited and pushed to main by the workflow. If there are no new changes to commit, the phrase "No new changes to commit" will be printed to the action logs.

## Connected workflows

None.