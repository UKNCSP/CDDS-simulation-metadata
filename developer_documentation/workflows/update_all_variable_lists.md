<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [update_all_variable_lists.yml](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/workflows/update_all_variable_lists.yml)

## Overview

This workflow is triggered by workflow dispatch only. It runs the script [update_all_variable_lists.py](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/scripts/update_all_variable_lists.py) to update all variable lists located in the current data request version directory of the [variables directory](https://github.com/UKNCSP/CDDS-simulation-metadata/tree/main/variables) e.g. if we are on data request version 1.2.2.5, it will update all variable lists under [variables/v1.2.2.5](https://github.com/UKNCSP/CDDS-simulation-metadata/tree/main/variables/v1.2.2.5). These files are automatically commited and pushed to main by the workflow.

## Connected workflows

None.