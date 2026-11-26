<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# Extending a Simulation
If a simulation has been extended beyond its currently registered date range, the simulation metadata must be updated before the additional data can be processed.

There are two cases:
- **Prepending data**: adding data **before** the currently registered start date.
- **Appending data**: adding data **after** the currently registered end date.

> **Important:** Only the newly added period should be processed. Do not reprocess the complete simulation date range.

## Prepending data
Use this process when data has been added **before the current start of the simulation**.

For example:
- Currently registered period: `1900–2100`
- Extended simulation period: `1850–2100`
- Period to process: `1850–1900`

### 1. Update the registered start date
Use the [modify workflow metadata](https://github.com/UKNCSP/CDDS-simulation-metadata/issues/new?template=modify_workflow_metadata.yml) issue form.

You will need to provide:
- the **workflow ID** (also known as the **suite ID**); and
- the new value for the simulation start date (for the example above, change the start date from `1900` to `1850`).

Submitting the issue will create a pull request containing the metadata change. A member of the CDDS team will review and merge this pull request.

> **Do not merge the pull request yourself.**

Wait until the pull request has been merged before continuing.

### 2. Generate a new CDDS request file
Once the metadata change has been merged, use the [generate CDDS request file](https://github.com/UKNCSP/CDDS-simulation-metadata/issues/new?template=generate_request_file.yml) issue form.

When completing the form:
- Set **Inventory Check** to `False`.
- Choose a **Package Name** that clearly identifies this run as an extension and distinguishes it from previous processing (e.g. `round-prepend_1850-1900`).

### 3. Restrict the request to the prepended period
Make a local copy of the generated request file and save it in your working directory.
The `start` and `end` values in the `[data]` section will initially describe the **complete extended simulation period**. Edit these values so that the request covers **only the data being prepended**.

For example:
| | Start | End |
|---|---|---|
| Original registered period | `1900` | `2100` |
| New registered period | `1850` | `2100` |
| **Request should process** | **`1850`** | **`1900`** |

Therefore:
- `start` = the **new simulation start date** (`1850`)
- `end` = the **previous simulation start date** (`1900`)

> **Important:** The boundary between the existing and extended data must match exactly. An incorrect boundary can lead to missing or overlapping data later in processing.


## Appending data
Use this process when data has been added **after the current end of the simulation**.

For example:
- Currently registered period: `1850–2100`
- Extended simulation period: `1850–2150`
- Period to process: `2100–2150`

The procedure is the same as for prepending, except that you update the **end date** and restrict processing to the period after the old end date.

### 1. Update the registered end date
Use the [modify workflow metadata](https://github.com/UKNCSP/CDDS-simulation-metadata/issues/new?template=modify_workflow_metadata.yml) issue form.

You will need to provide:
- the **workflow ID** (also known as the **suite ID**); and
- the new simulation end date (for the example above, change the end date from `2100` to `2150`).

Submitting the issue will create a pull request containing the metadata change. A member of the CDDS team will review and merge this pull request.

> **Do not merge the pull request yourself.**

Wait until the pull request has been merged before continuing.

### 2. Generate a new CDDS request file
Once the metadata change has been merged, use the [generate CDDS request file](https://github.com/UKNCSP/CDDS-simulation-metadata/issues/new?template=generate_request_file.yml) issue form.

When completing the form:
- Set **Inventory Check** to `False`.
- Choose a **Package Name** that clearly identifies this run as an extension and distinguishes it from previous processing (e.g. `round-append_2100-2150`).

### 3. Restrict the request to the appended period
Make a local copy of the generated request file and save it in your working directory.

The `start` and `end` values in the `[data]` section will initially describe the **complete extended simulation period**. Edit these values so that the request covers **only the newly appended data**.

For example:
| | Start | End |
|---|---|---|
| Original registered period | `1850` | `2100` |
| New registered period | `1850` | `2150` |
| **Request should process** | **`2100`** | **`2150`** |

Therefore:
- `start` = the **previous simulation end date** (`2100`)
- `end` = the **new simulation end date** (`2150`)

> **Important:** The boundary between the existing and extended data must match exactly. An incorrect boundary can lead to missing or overlapping data later in processing.

## Quick reference

| Extension type | Metadata to change | Request start | Request end |
|---|---|---|---|
| **Prepend** | Simulation start date | New start date | Previous start date |
| **Append** | Simulation end date | Previous end date | New end date |

In both cases:
1. Update the registered simulation metadata.
2. Wait for the resulting pull request to be reviewed and merged.
3. Generate a new CDDS request file.
4. Set **Inventory Check** to `False`.
5. Give the package a name that clearly identifies the extension.
6. Edit the `[data]` date range so that **only the newly added period is processed**.
7. Double-check that the extension boundary exactly matches the previously processed period.