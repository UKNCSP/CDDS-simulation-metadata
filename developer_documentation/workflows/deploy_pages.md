<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [deploy_pages.yml](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/workflows/deploy_pages.yml)

## Overview

This workflow is triggered by the successful completion of on a cron schedule or via workflow dispatch. This workflow simply runs scripts/generate_metadata_tables.py and scripts/metadata_per_mip.py then triggers the mkdocs deployment. For instructions on how to deploy pages from the command line, see [Updating Documentation For Developers](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/developer_documentation/updating_documentation.md).

> !!! Note
> This workflow will trigger a secondary workflow on its completion which builds and deploys the documentation. This may take several minutes to complete.

## Connected workflows

None.