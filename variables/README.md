<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
## Variable lists

> **NOTE:** 
>  Do not edit any files directly within the repository. To make changes to any file, you must first download it and only make edits to your local copy.**

The variable lists in this folder are specifically designed to correspond to a workflow metadata submission created using the `Add/Modify Workflow Metadata` issue form.

We use the model and experiment specified in the workflow metadata submission to pre-identify the status of each variable available within the experiment (for example, approved, embargoed, do-not-produce, etc.).

Please always use the variable list contained within the most recent version folder, unless otherwise advised by a member of the CDDS team. This should align with the current version of the data request process that is being used.

Variable lists are updated periodically to incorporate newly approved variables and to ensure that any variables which cannot be produced are clearly marked. If you are aware of a recently approved variable that you wish to produce, but it is not listed as "approved" in the variable list, please open a blank issue. A member of the CDDS team will regenerate the relevant files and ensure that the variable list is updated accordingly.

The name of the corresponding request will have been left as a comment on the issue created when you submitted your workflow metadata using the `Add/Modify Workflow Metadata` issue form. Please note that this issue will likely have been closed. Alternatively, you can identify the correct variable list by locating the file whose name begins with the corresponding model workflow ID. The variable list filename will also contain the experiment ID and model ID from the workflow metadata submission.

For example, for the workflow metadata file [u-dv341.cfg](../workflow_metadata/u-dv341.cfg), the corresponding variable list is [u-dv341_piControl_UKCM2-0-LL.txt](v1.2.2.4/u-dv341_piControl_UKCM2-0-LL.txt).

> **CAUTION:** 
>  To produce any non-approved variables, you will need to manually uncomment them within the variable list. However, variables that are not marked as approved may not be producible. If they do produce without triggering critical errors, please be aware that the output has not been checked or verified, either through automated processes or by a member of the team.**