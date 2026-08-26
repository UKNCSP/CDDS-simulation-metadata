<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [generate_request.yml](../../../.github/workflows/generate_request.yml)

## Overview

This workflow is triggered when a user fills out the [Request The Generation of A CDDS Request File](../../../.github/ISSUE_TEMPLATE/generate_request_file.yml) issue form. The workflow triggers the script [generate_request.py](../../../scripts/generate_request.py) which formats a ready to go Met Office or JASMIN request based off of the form content. This is then automatically commited and pushed to the [requests directory](../../../requests) with a filename formatted as `<request_type>_<model_workflow_id>_<package>.cfg`.

These requests are then picked up by users for use in production. For each new round of a given workflow, the user should generate a new request file. If a change needs to be made to a request that has already been generated, it is up to the discretion of the CDDS team member whether they choose to:
1. Delete the existing request and have the user re fill out the [Request The Generation of A CDDS Request File](../../../.github/ISSUE_TEMPLATE/generate_request_file.yml) issue form with the correct streams/package etc...
2. Manually update the existing request with the new information. In this case, an informative commit message should be given (noting what was updated in the request) so that we have a clear record of what has changed. **Manual changes should only be done by CDDS team members** to ensure that all changes are properly recorded.



> **!! Important !!**
> Under no circumstances should any metadata fields be manually updated in a request. Changes to any metadata field, the start_date, end_date, mass_data_class, mass_ensemble_member or atmospheric_timestep must be completed at the workflow_metadata level so that this can be propagated through to the request appropriately. See the [updating metadata](../../../docs/developer_documentation/updating_metadata.md) docs for further guidence on this process.

## Connected workflows

None.