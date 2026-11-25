<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.-->

# Updating Documentation For Developers

This repository houses two categories of documentation:
1. The developer documentation: this is a set of markdown files stored in the [developer_documentation directory](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/developer_documentation/). These are intended to explain the code functionality of any scripts, processes or GitHub actions on this repositroy and are not intended for users. These are stored as markdown files and are not deployed to GitHub pages.
2. User documentation and information: this is information intended to support users of the CDDS-simulation-metadata stored as a separate set of markdown files in the [docs directory](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/docs/). This support includes some brief "how to" type instructions as well as general information about CMIP7 processes, variables, models and MIPs. This information is hosted on GitHub pages through `mkdocs`. The pages can be seen here https://ukncsp.github.io/CDDS-simulation-metadata/.

## Updating Developer Documentation

Any updates to developer documentation can be applied by simply creating a branch and pull request to apply your changes.

> **!!! Important**:
> Although not hosted on GitHub pages, this developer documentation is still public. Caution should be taken to ensure no sensitive information such as explicit paths is included. 

Please ensure that pull requests are reviewed by at least one other person or using GitHub CoPilot (see the [Use Of Generative AI Policy](https://github.com/UKNCSP/CDDS-simulation-metadata#use-of-generative-ai/)) to check for spelling/gramatical errors and ensure that any instructions are clear.

## Updating User Documentation/Pages

As with developer documentation, any updates under the docs directory should be done through the usual branching and pull request proceedure. Pull requests to update documentation may also come from users wishing to add additional information about their model/MIP.

Please ensure that pull requests are reviewed by at least one other person or using GitHub CoPilot (see the [Use Of Generative AI Policy](https://github.com/UKNCSP/CDDS-simulation-metadata#use-of-generative-ai/)) to check for spelling/gramatical errors and ensure that any instructions are clear.

### Deploying Pages

Once the pull request has been approved and merged to main, the pages must be re deployed so that the changes are applied. This happens on a regular cron schedule, however, there are also various ways of triggering this on demand. 

1. The [deploy_pages](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/workflows/deploy_pages.yml) workflow can be triggered through workflow dispatch. To trigger this, navigate to the associated[GitHub actions page](https://github.com/UKNCSP/CDDS-simulation-metadata/actions/workflows/deploy_pages.yml) and hit the green "Run workflow" button in the top right of the screen ensuring that "Run workflow from main" is selected. Go [here](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/.github/developer_documentation/workflows/deploy_pages.md) for more information on what this workflow does. 

    > !!! Note
    > This workflow will trigger a secondary workflow on its completion which builds and deploys the documentation. This may take several minutes to complete.

2. The process to deploy the pages can also be completed from the command line by running the following commands from an up to date version of main. Please ensure you run `git pull` before deploying the documentation to include all new changes. 
    > !!! Note
    > You will need to activate the CDDS developer environment before running the following commands.

    `mike deploy docs`

    `git push origin gh-pages`