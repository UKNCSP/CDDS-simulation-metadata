# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Notes all workflows currently registered for a given MIP and populates the associated `docs/mips/*.md` file with a
table containing their basic information."""

import configparser

from constants import WORKFLOW_METADATA_DIR, REQUESTS_DIR, MIP_DOCS_DIR

MARKDOWN_TABLE_TITLE = "## Simulations Currently Registered For This MIP"
MARKDOWN_TABLE_HEADER = ["\n", "| Simulation | Model Workflow ID | In Processing? |\n", "| ----- | ----- | ----- |\n"]
TICK = "✅"
CROSS = "❌"


def get_all_workflow_metadata() -> list:
    """Returns a list of the paths of all workflow metadata configuration files within the repository.

    Returns
    -------
    list
        A list of all workflow metadata configuration files.
    """
    return list(WORKFLOW_METADATA_DIR.glob('*.cfg'))


def update_workflow_info_for_mip(metadata_config, workflow_mips_dict):
    mip = (metadata_config["metadata"]["mip"]).lower()
    model = metadata_config["metadata"]["model_id"]
    experiment = metadata_config["metadata"]["experiment_id"]
    variant = metadata_config["metadata"]["variant_label"]
    workflow_id = metadata_config["data"]["model_workflow_id"]
    in_processing = TICK if check_for_request(workflow_id) is True else CROSS

    if mip not in workflow_mips_dict:
        workflow_mips_dict[mip] = []
    workflow_mips_dict[mip].append(
        f"| {model} {experiment} {variant} | [{workflow_id}]"
        f"(https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/workflow_metadata/{workflow_id}.cfg) | "
        f"{in_processing} |\n"
    )


def check_for_request(workflow_id):
    all_requests = list(REQUESTS_DIR.glob('*.cfg'))
    for request_filename in all_requests:
        if f"_{workflow_id}_" in str(request_filename):
            return True

    return False


def read_doc(doc):
    with open(doc, "r") as file:
        lines = [line for line in file]

    return lines


def restruct_dict_to_table(workflow_mips_dict, mip):
    table_data = MARKDOWN_TABLE_HEADER
    for mip in workflow_mips_dict:
        info = workflow_mips_dict.get(mip)
        for entry in sorted(info):
            table_data.append(entry)

    return table_data


def update_doc(doc, table_data):
    old_doc_format = read_doc(doc)
    for i, line in enumerate(old_doc_format):
        if MARKDOWN_TABLE_TITLE in line:
            table_removed = old_doc_format[:i]

    new_doc_format = table_removed + [MARKDOWN_TABLE_TITLE] + table_data
    with open(doc, "w", encoding="utf-8") as f:
        for line in new_doc_format:
            f.write(line)


def main():
    workflow_mips_dict = {}
    all_workflows = get_all_workflow_metadata()
    for file in all_workflows:
        metadata_config = configparser.ConfigParser()
        metadata_config.read(file)
        update_workflow_info_for_mip(metadata_config, workflow_mips_dict)

    mip_docs = list(MIP_DOCS_DIR.glob('*.md'))
    for doc in mip_docs:
        mip = str(doc).split("/")[-1].strip(".md")
        if mip in workflow_mips_dict:
            table_data = restruct_dict_to_table(workflow_mips_dict, mip)
        else:
            table_data = ["\n", "\n", "No workflows/simulations are currently registered for this MIP."]

        update_doc(doc, table_data)


if __name__ == "__main__":
    main()
