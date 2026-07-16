<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
> **IMPORTANT:
>  Do not edit any files directly within the repository. To make changes to any file, you must first download it and only make edits to your local copy.**

> **CAUTION: 
>  To produce any non-approved variables, you will need to manually uncomment them within the variable list. However, variables that are not marked as approved may not be producible. If they do produce without triggering critical errors, please be aware that the output has not been checked or verified, either through automated processes or by a member of the team.**

## Finding Your Variable List
The variable lists in this folder are specifically designed to correspond to a workflow metadata submission created using the `Add/Modify Workflow Metadata` issue form. These are generated at the point of submission. The name of the corresponding variable list will have been left as a comment on the issue created when you submitted your workflow metadata using the `Add/Modify Workflow Metadata` issue form and under any request file generation issue created using the `Request The Generation Of A CDDS Request File` issue form. Please note that these issues will likely have been closed. Alternatively, you can identify the correct variable list by locating the file whose name begins with the corresponding model workflow ID. The variable list filename will also contain the experiment ID and model ID from the workflow metadata submission. For example, for the workflow metadata file [u-dv341.cfg](../workflow_metadata/u-dv341.cfg), the corresponding variable list is [u-dv341_piControl_UKCM2-0-LL.txt](v1.2.2.4/u-dv341_piControl_UKCM2-0-LL.txt).

> **IMPORTANT:
>  Please always use the variable list contained within the most recent version folder, unless otherwise advised by a member of the CDDS team. This should align with the current version of the Data Request that is being used.**

## Understanding the Variable List
We use the model and experiment specified in the workflow metadata submission to pre-identify the status of each variable available within the experiment (for example: approved, embargoed or do-not-produce). Not every experiment or model is able to produce every variable.

> **NOTE:
>  Variable lists are updated periodically to incorporate newly approved variables and to ensure that any variables which cannot be produced are clearly marked. If you are aware of a recently approved variable that you wish to produce, but it is not listed as "approved" in the variable list, please open a blank issue. A member of the CDDS team will regenerate the relevant files and ensure that the variable list is updated accordingly.**

### Variable naming conventions
The convention for naming variables has changed substantially since CMIP6. In CMIP7 the "branded variable" system was introduced to provide greater detail about the temporal and spatial sampling of the variable directly within its name.

For example, `Amon.tas` (as it was known in CMIP6) is now shown in the variable list as `atmos/tas_tavg-h2m-hxy-u@mon`. This can be broken down generally into `<realm>/<variable_name>_<temporal_label>-<vertical_label>-<horizontal_label>-<area_type_label>@<frequency>`. Hence, following on from our example of `Amon.tas`, we can immediately tell the following about the variable:
| key | Value |
| ----- | ----- |
| realm | atmos (atmospheric) |
| variable name | tas |
| temporal label | tavg (time average) |
| vertical label | h2m (near surface, specifically 2 meters above ground) |
| horizontal label | hxy (horizontal latitude-longitude grid) |
| area type label | u (unmasked) |
| frequency | mon (monthly) |

### Variable Status Comments And What They Mean

Within the variable list, each variable may have one or more inline comments next to it. This provides information on the status and priority of that variable. Any approved variables with no `priority=` type label can be assumed to be listed as either 'high' or 'core' priority in the current version of the Data Request. See the table below for more information about what each label means for you.

| Status Label | Meaning | 
| ----- | ----- |
| `approved`| We have confirmed that we are able to produce this variable and its output has been verified either by our automatic diagnostic review process or manually by a person. |
| `embargoed` | We have not yet been able to confirm whether this variable is producible or verify its output. |
| `do-not-produce`| This variable cannot be produced, attempting to do so will result in critical errors or an invalid output. |
| `do-not-produce (not available with this model)` | This variable cannot be produced using the given experiment or model | 
| `known-issue` | This variable is known to have an issue. This may be revisited in time to see if a fix can be applied. |
| `Yearly variables unable to be processed at this time` | We are currently unable to produce variables at a yearly frequency. Attempting to do so will result in critical errors. |
| `unknown (no stream information available)` | This variable is missing stream information and hence cannot currently be produced. |
| `no-mapping-found` | This variable has no mapping information and hence cannot currently be produced. |
| `priority=medium` | This variable is listed as 'medium' priority in the current version of the Data Request. |
| `priority=low` | This variable is listed as 'low' priority in the current version of the Data Request. |



