# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Notes all workflows currently registered for a given MIP and populates the associated `docs/mips/*.md` file with a
table containing their basic information."""

import configparser

from pathlib import Path

from constants import WORKFLOW_METADATA_DIR, REQUESTS_DIR, MIP_DOCS_DIR

MARKDOWN_TABLE_TITLE = "## Simulations Currently Registered For This MIP"
MARKDOWN_TABLE_HEADER = ["\n", "| Simulation | Model Workflow ID | In Processing? |\n", "| ----- | ----- | ----- |\n"]
TICK = "✅"
CROSS = "❌"


def glob_directory(directory: Path, file_suffix: str) -> list:
    """Returns a list of the paths of all of a given file type within a given directory in the repository.

    Parameters
    ----------
    directory: Path
        The directory to search in.
    file_suffix: str
        The file type to search for (e.g. cfg).

    Returns
    -------
    list
        A list of files of the given type in the given directory.
    """
    return list(directory.glob(f'*{file_suffix}'))


def update_workflow_info_for_mip(metadata_config: configparser.ConfigParser, workflow_mips_dict: dict) -> None:
    """Pulls the mip, model, experiment, variant label and workflow ID from a single config file in
    `workflow_metadata/*.cfg` and adds the information (along with whether it is currently being used in CMIP7
    processing) to a dictionary organised by mip.

    Parameters
    ----------
    metadata_config: configparser.ConfigParser
        The worflow metadata config file as a config object.
    workflow_mips_dict: dict
        The dictionary of key workflow information organised by mip.
    """
    # Pull key workflow/simulation information from the config file.
    mip = (metadata_config["metadata"]["mip"]).lower()
    model = metadata_config["metadata"]["model_id"]
    experiment = metadata_config["metadata"]["experiment_id"]
    variant = metadata_config["metadata"]["variant_label"]
    workflow_id = metadata_config["data"]["model_workflow_id"]
    in_processing = TICK if check_for_request(workflow_id) is True else CROSS

    # Create the mip key in the dict if it does not already exist.
    if mip not in workflow_mips_dict:
        workflow_mips_dict[mip] = []
    # Update `workflow_mips_dict` with the key info where the key is the mip.
    workflow_mips_dict[mip].append(
        f"| {model} {experiment} {variant} | [{workflow_id}]"
        f"(https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/workflow_metadata/{workflow_id}.cfg) | "
        f"{in_processing} |\n"
    )


def check_for_request(workflow_id: str) -> bool:
    """Checks if a given workflow ID has a corresponding request file in `requests/*.cfg` and hence whether it is being
    / has been used in processing.

    Parameters
    ----------
    workflow_id: str
        The model workflow ID to check for in  `requests/*.cfg`.

    Returns
    -------
    bool
        `True` if a request file referencing the given workflow ID exists, `False` if not.
    """
    all_requests = glob_directory(REQUESTS_DIR, ".cfg")
    for request_filename in all_requests:
        if f"_{workflow_id}_" in str(request_filename):
            return True

    return False


def read_doc(doc: Path) -> list[str]:
    """Reads in a single *.md file in its original state as a list of lines.

    Parameters
    ----------
    doc: Path
        The path to the .md file to read.

    Returns
    -------
    list[str]
        The .md file content where each line is a new item in the list.
    """
    with open(doc, "r") as file:
        lines = [line for line in file]

    return lines


def restruct_dict_to_table(workflow_mips_dict: dict, mip: str) -> list[str]:
    """Restructures the `workflow_mips_dict` containing the key information for each workflow categorised by mip into a
    markdown table for a single mip.

    Parameters
    ----------
    workflow_mips_dict: dict
        The dictionary of key workflow information organised by mip.
    mip:
        The MIP to create a markdown table for.

    Returns
    -------
    list[str]
        A markdown style table of the key information for workflows associated with the given mip where each item in the
        list is a new line.
    """
    table_data = MARKDOWN_TABLE_HEADER
    for mip in workflow_mips_dict:
        # Get the information for only the given MIP.
        info = workflow_mips_dict.get(mip)
        for entry in sorted(info):
            table_data.append(entry)

    return table_data


def update_doc(doc: Path, table_data: list[str]) -> None:
    """Removes the old table from a single `docs/mips/*.md` file and replaces it with the updated table constructed in
    `restruct_dict_to_table()`.

    Parameters
    ----------
    doc: Path
        The path to the .md file to update.
    table_data: list[str]
        A markdown style table of the key information for workflows associated with the given mip where each item in the
        list is a new line.
    """
    old_doc_format = read_doc(doc)
    for i, line in enumerate(old_doc_format):
        # Identify where the table title exists in the original doc and remove the old version of the table.
        if MARKDOWN_TABLE_TITLE in line:
            table_removed = old_doc_format[:i]

    # Append the new table onto the .md file. This table should always be at the base of the .md to avoid loosing
    # information between updates.
    new_doc_format = table_removed + [MARKDOWN_TABLE_TITLE] + table_data
    with open(doc, "w", encoding="utf-8") as f:
        for line in new_doc_format:
            f.write(line)


def main():
    """Main."""
    workflow_mips_dict = {}
    all_workflows = glob_directory(WORKFLOW_METADATA_DIR, ".cfg")
    for file in all_workflows:
        # Read in each config file in `workflow_metadata/*.cfg` and extract key info.
        metadata_config = configparser.ConfigParser()
        metadata_config.read(file)
        update_workflow_info_for_mip(metadata_config, workflow_mips_dict)

    mip_docs = glob_directory(MIP_DOCS_DIR, ".md")
    for doc in mip_docs:
        # Open each MIP documentation page and note each workflow metadata that is currently registered under that MIP.
        mip = str(doc).split("/")[-1].strip(".md")
        if mip in workflow_mips_dict:
            # If workflows are registered for the MIP, provide their key information and processing status as a table.
            table_data = restruct_dict_to_table(workflow_mips_dict, mip)
        else:
            # If no workflows are registered for the MIP, state this.
            table_data = ["\n", "\n", "No workflows/simulations are currently registered for this MIP."]

        update_doc(doc, table_data)


if __name__ == "__main__":
    main()
