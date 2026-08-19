# process_new_metadata.yml

## Overview

The [process_new_metadata.yml](../../../.github/workflows/process_new_metadata.yml) workflow automates the processing of newly submitted simulation metadata.

When a user submits an issue form to add or modify workflow metadata, this workflow validates the submission, generates the metadata configuration file and variable list, updates the metadata tables hosted on github pages, pushes new files directly to main, and notifies users of the output of their submission in real time. This workflow is designed to blend efficiency and accuracy, putting the power to drive changes into the hands of the users but in a way that ensure the information given is accurate, controlled, verified and tracable.

This workflow is triggered when any issue with the label `metadata entry` is created or editted. This label is automatically applied when users fill out the [add_workflow_metadata](../../../.github/ISSUE_TEMPLATE/add_workflow_metadata.yml) issue form.

![image](../../../docs/developer_documentation/workflows/add_workflow_metadata_flowchart)

## Workflow Inputs

| Input | Required | Description |
|---------|---------|-------------|
| `<input_name>` | Yes | Description of input. |
| `<input_name>` | No | Description of input. |

## Jobs

### 1. Validation

#### Purpose

Ensures the submitted metadata is complete and correctly formatted.

#### Actions

- Check required fields.
- Validate schema.
- Verify workflow identifiers.
- Confirm repository conventions are met.

#### Failure Behaviour

If validation fails:

- Workflow stops.
- Error details are reported to the user.
- No repository changes are made.

---

### 2. Metadata Processing

#### Purpose

Transforms user-provided metadata into repository-managed files.

#### Actions
- Parse submission data.
- Generate workflow metadata files.
- Apply standard formatting.
- Store outputs in the appropriate directory.

#### Outputs

| Output | Description |
|----------|-------------|
| Metadata file | Generated workflow metadata record. |

---

### 3. Derived Artefact Generation

#### Purpose

Updates generated content that depends on workflow metadata.

#### Examples

- Metadata tables.
- Search indices.
- Variable lists.
- Documentation pages.

#### Outputs

| Output | Description |
|----------|-------------|
| Generated tables | Updated metadata summary tables. |
| Generated files | Additional derived artefacts. |

---

### 4. Repository Update

#### Purpose

Commits generated changes back to the repository.

#### Actions

- Configure git credentials.
- Commit generated files.
- Push updates to the main branch.

#### Commit Message Format

```text
Automated update from metadata submission
```

*(Replace with actual commit message used by workflow.)*

---

## Repository Locations

### Inputs

| Path | Description |
|---------|-------------|
| `workflow_metadata/` | Source metadata records. |
| `reference_information/` | Supporting reference information. |

### Outputs

| Path | Description |
|---------|-------------|
| `metadata_tables/` | Generated metadata summaries. |
| `docs/` | Published documentation assets. |

## Dependencies

### GitHub Actions

| Action | Purpose |
|----------|---------|
| `actions/checkout` | Retrieve repository contents. |
| `<action>` | `<purpose>` |

### Python Scripts

| Script | Purpose |
|---------|---------|
| `<script_name>.py` | Description. |

## Error Handling

The workflow will fail if:

- Required metadata is missing.
- Metadata schema validation fails.
- Generated outputs cannot be created.
- Repository updates cannot be committed.

Common troubleshooting steps:
 
1. Verify the submission contains all required fields.
2. Check workflow logs in GitHub Actions.
3. Confirm generated files are valid.
4. Re-run the workflow after correcting issues.
 
## Permissions
 
The workflow requires permissions to:
 
- Read repository contents.
- Write generated files.
- Create commits.
- Update issues or comments.
 
## Monitoring
 
GitHub Actions logs can be viewed at:
 
```text
Actions → process_new_metadata
```
 
Key log sections:
 
- Validation
- Metadata generation
- Artefact generation
- Repository updates
 
## Related Documentation
 
- Repository README
- Metadata submission process
- Workflow metadata schema
- CMIP7 operational procedure
 
## Maintenance Notes
 
When modifying this workflow:
 
1. Preserve backward compatibility where possible.
2. Update this documentation if triggers or jobs change.
3. Test changes using a development branch before merging.
4. Ensure generated artefacts remain reproducible.