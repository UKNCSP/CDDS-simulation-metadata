
<!--(C) British Crown Copyright 2025-2026, Met Office. Please see LICENSE.md for license details.-->
# CDDS Simulation Metadata For CMIP7
[![Deploy static content to Pages](https://github.com/UKNCSP/CDDS-simulation-metadata/actions/workflows/deploy_pages.yml/badge.svg)](https://github.com/UKNCSP/CDDS-simulation-metadata/actions/workflows/deploy_pages.yml)

CURRENT MAPPINGS FILE VERSION: v2026-11-06

CURRENT DATA REQUEST VERSION: 1.2.2.5

CURRENT CDDS RELEASE VERSION: v4.0.6

This CDDS simulation metadata repository is designed to process and store CMIP7 workflow metadata. If you have a new
workflow that you wish to register, please fill out the issue form marked 'Add/Modify Workflow Metadata'. Upon form
completion, you will receive a notification from our GitHub actions bot confirming your submission. If you wish to view
the workflow metadata currently stored in the database, you can do so here:
[CMIP7 Workflow Metadata](https://ukncsp.github.io/CDDS-simulation-metadata/metadata_tables/). Note that this table
consists of only key metadata: to view the full metadata, click the link shown on the model workflow ID of interest. Any
new additions may take up to an hour to become available to view and search on
[CMIP7 Workflow Metadata](https://ukncsp.github.io/CDDS-simulation-metadata/metadata_tables/).

> **IMPORTANT:
>  Do not edit any request or variable list files directly within the repository. Do not merge any pull requests without
review from a CDDS team member. To make any changes, you must first download it and only make edits to your local copy.
If you need to update or remove information within a workflow metadata configuration file, please open an issue and
include the relevant model workflow ID, along with a clear description of the requested change.**

## Use Of Generative AI
This repository may contain code that has been written by or with the assistance of Generative AI. Only GenAI tools that
have been approved for use by the Met Office may be used. These currently include the Met Office's enterprise licensed
Github Copilot and Met Office Enterprise M365 Copilot. Personal or individually licensed Copilot accounts are not
approved for use on this repository. The Met Office reserves the right to revoke the approval of any GenAI tool at any
time for any reason.

Note: You must verify and amend as necessary all GenAI output that you intend to incorporate into CDDS as you would any
non-AI assisted content you produce. For example: editing, proof reading, sense checking, code review, testing,
vulnerability scanning etc.

## Registering Workflow Metadata
To register the metadata for a new workflow or edit the metadata for an existing workflow, please navigate to the issue
tab at the top of the page, click "new issue" and select "Add/Modify Workflow Metadata". This will open up an issue form
for you to fill in. Once filled in , click the create button in the bottom right of the page. This will open an issue
that will be automatically validated and processed. You will recieve an email from the github actions bot upon
completion confirming your workflow registration and the closure of the issue (this typically takes up to a few
minutes). Any errors will be communicated to you by the github actions bot in the comments of your issue which will
remain open. If you make an error on your issue form, please edit the issue body with your changes or submit a new form
containing the correct information. This will create a pull request that will be reviewed by a member of our team.
It would be valuable to us if a brief comment could be left on the pull request explaining the reason for the change.
For additional user guidance please see the wiki or our
[GitHub pages](https://ukncsp.github.io/CDDS-simulation-metadata/).
