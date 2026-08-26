<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [update_webview.yml](../../../.github/workflows/update_webview.yml)

## Overview

This workflow is triggered on a daily cron schedule at midnight (UCT) or via workflow dispatch. Its role is simply to run the script [generate_metadata_tables.py](../../../scripts/generate_metadata_tables.py). This generates a searchable html table using every `<workflow_id>.cfg` file present in the [workflow metadata](../../../workflow_metadata) directory (where each row of the table accounts for a single cfg file). The generated table is saved as [index.html](../../../metadata_tables/index.html).


## Connected workflows

The successful completion of this workflow will automatically trigger [deploy_pages.yml](../../../.github/workflows/deploy_pages.yml) (see docs [here](../../../docs/developer_documentation/workflows/deploy_pages.md)). 