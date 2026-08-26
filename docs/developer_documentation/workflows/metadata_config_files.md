<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# [process_new_metadata.yml](../../../.github/workflows/process_new_metadata.yml)

## Overview

The [process_new_metadata.yml](../../../.github/workflows/process_new_metadata.yml) workflow automates the processing of newly submitted simulation metadata.

When a user submits the [Add/Modify Workflow Metadata](../../../.github/ISSUE_TEMPLATE/add_workflow_metadata.yml) issue form to register workflow metadata, this workflow validates the submission, generates the metadata configuration file, generates a variable list, updates the metadata tables hosted on github pages, pushes new files directly to main, and notifies users of the outcome of their submission in real time. This workflow is designed to blend efficiency and accuracy, putting the power to drive changes into the hands of the users in a way that ensures accurate, verifiable and tracable information.

This workflow is triggered when any issue with the label `metadata entry` is created or editted. This label is automatically applied when users fill out the [Add/Modify Workflow Metadata](../../../.github/ISSUE_TEMPLATE/add_workflow_metadata.yml) issue form.

![image](../../../docs/developer_documentation/workflows/add_workflow_metadata_flowchart.png)


#### File Outputs

| Output | Naming convention |Description |
|----------|-------------| -------------|
| Metadata configuration file | `workflow_metadata/<model_workflow_id>.cfg` | Organised record of workflow metadata for a single model workflow ID. |
| Variable list text file | `variables/<data_request_version>/<model_workflow_id>_<experiment>_<model>.txt` | A complete variable list for the given model and experiment with approved variables automatically uncommented. |

---
 
## Connected workflows

None.