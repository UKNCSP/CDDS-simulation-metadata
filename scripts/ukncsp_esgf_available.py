# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Audits all CMIP7 global variables to determine their availability on esgf and for which members."""

import requests

from pathlib import Path

from common import read_json
from constants import (MAPPINGS_FILE_LOCATION, CELL_TEMPLATE, HEADER_ROW_TEMPLATE, BGCOLORS, HYPERLINK, ROW_TEMPLATE,
                       TABLE_TEMPLATE, HEADER, LAST_UPDATED, FOOTER, KNOWN_ISSUES_DICT_FILE_LOCATION)

ESGF_ARCHIVE_LINK = ("https://discovery.east.esgf.io/search?collections=CMIP7&limit=1000&filter=%7B%22op%22%3A%22and%22"
                     "%2C%22args%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22args%22%3A%5B%7B%22property%22%3A%22properties.cm"
                     "ip7%3Aarea_label%22%7D%2C%22{}%22%5D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22args%22%3A%5B%7B%22propert"
                     "y%22%3A%22properties.cmip7%3Ahorizontal_label%22%7D%2C%22{}%22%5D%7D%2C%7B%22op%22%3A%22%3D%22%2C"
                     "%22args%22%3A%5B%7B%22property%22%3A%22properties.cmip7%3Ainstitution_id%22%7D%2C%22UKNCSP%22%5D%"
                     "7D%2C%7B%22op%22%3A%22%3D%22%2C%22args%22%3A%5B%7B%22property%22%3A%22properties.cmip7%3Atemporal"
                     "_label%22%7D%2C%22{}%22%5D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22args%22%3A%5B%7B%22property%22%3A%22"
                     "properties.cmip7%3Avariable_id%22%7D%2C%22{}%22%5D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22args%22%3A%5"
                     "B%7B%22property%22%3A%22properties.cmip7%3Avertical_label%22%7D%2C%22{}%22%5D%7D%2C%7B%22op%22%3A"
                     "%22%3D%22%2C%22args%22%3A%5B%7B%22property%22%3A%22properties.latest%22%7D%2C%22true%22%5D%7D%5D%"
                     "7D&filter-lang=cql2-json")
CLIMATE_RESOURCE_LINK = "https://www.climate-resource.com/tools/esm-model/cmip7-availability/variables/{}"
HEADINGS = ["Variable", "BCV", "Model", "Published", "Experiment", "Variant", "Start Date", "End Date"]
CMIP7_MODELS = ["UKCM2-0-LL", "UKCM2a-0-HH", "UKESM1-3-LL"]
TICK = "✅"
CROSS = "❌"
ISSUE = "⚠️"


def filter_esgf_archive(branded_variable: str) -> list[dict]:
    """Filters information under published data for a given variable in the ESGF searchable metagrid constrained for
    UKNCSP data.

    Parameters
    ----------
    branded_variable: str
        The variable to check for on ESGF.

    Returns
    -------
    list[dict]
        A list of dictionaries where each dict corresponds to a member within ESGF for the given variable.
    """
    # Split branding facets for use in filtering.
    variable_id, branding = branded_variable.split("_")
    temporal_label, vertical_label, horizontal_label, area_label = branding.split("-")
    # Pull the filtered information down from ESGF.
    esgf = requests.get(
        ESGF_ARCHIVE_LINK.format(area_label, horizontal_label, temporal_label, variable_id, vertical_label)).json()

    # Filter out the key information from each member.
    published_data = []
    datasets = esgf.get("features")
    for member in datasets:
        published_data.append({
            "var": member["properties"].get("cmip7:variable_branded_name"),
            "freq": member["properties"].get("cmip7:frequency"),
            "model": member["properties"].get("cmip7:source_id"),
            "exp": member["properties"].get("cmip7:experiment_id"),
            "variant": member["properties"].get("cmip7:variant_label"),
            "start": member["properties"].get("start_datetime"),
            "end": member["properties"].get("end_datetime")
        })

    return published_data


def get_all_glb_variables() -> list[str]:
    """Returns a list of all global CMIP7 variables present in `reference_information/mappings.json`.

    Returns
    -------
    list[str]
        A list of all global CMIP7 variables.
    """
    mappings = read_json(MAPPINGS_FILE_LOCATION)
    variables = []
    for mapping in mappings:
        variable = mapping.get("branded_variable")
        if variable.endswith(".glb"):
            variables.append(variable)

    return variables


def check_if_bcv(variable: str) -> bool:
    """Identifies whether a given variable is a BCV (baseline climate variable).

    Parameters
    ----------
    variable: str
        The variable to check.

    Returns
    -------
    bool
        `True` if the given variable is a BCV, `False` if not.
    """
    mappings = read_json(MAPPINGS_FILE_LOCATION)
    for mapping in mappings:
        if mapping.get("branded_variable") == variable:
            if "BCV" in mapping.get("labels"):
                return True

    return False


def check_if_known_issue(variable: str, model: str) -> bool:
    """Checks if the variable is in the known issues list for a given model.

    Parameters
    ----------
    variable: str
        The variable to check.
    model: str
        The model to check.

    Returns
    -------
    bool
        `True` if variable is in the known issues, `False` if not.
    """
    known_issues = read_json(KNOWN_ISSUES_DICT_FILE_LOCATION)
    realm, var, brand, freq, _ = variable.split(".")
    issues_for_model = []

    # Get a list of all variables in the known issues for the given model regardless of experiment or variant
    filtered_dict = [v for v in known_issues[model].values() if isinstance(v, dict)]
    for v in filtered_dict:
        issues_for_model = issues_for_model + list(v["*"].keys())

    if f"{realm}/{var}_{brand}@{freq}" in issues_for_model:
        return True
    else:
        return False


def search_available_models(branded_var: str, freq: str) -> list[str]:
    """Returns a list of CMIP7 models that a given variable is producible with.

    Parameters
    ----------
    branded_var: str
        The branded variable name to check.
    freq: str
        The frequency of the branded variable to check.

    Returns
    -------
    list[str]
        A list of CMIP7 models that the variable can be produced with.
    """
    available_models = []
    for model in CMIP7_MODELS:
        var_name = f"{".".join(branded_var.split("_"))}.{freq}.glb"
        # Identify the base model used in naming `reference_information` variable status json files.
        if model in ("UKCM2-0-LL", "UKCM2a-0-HH"):
            base_model = "UKCM2"
        elif model == "UKESM1-3-LL":
            base_model = "UKESM1-3"
        else:
            raise RuntimeError(f"Model {model} not recognised.")

        model_info = read_json(f"reference_information/{base_model}_variable_status.json")
        for variable, status in model_info.items():
            # Check the status assigned to each variable to determine which variables are theoretically producible with
            # this model regardless of approval status.
            if var_name in variable and status in ("approved", "embargoed"):
                available_models.append(model)

    return available_models


def generate_table_data() -> list[list]:
    """Generates the data to populate the table.

    Returns
    -------
    list[list]
        The table content where as a list of lists, where each list is the data for a single row.
    """
    variables = get_all_glb_variables()
    table_data = []
    for variable in variables:
        # Separate out the key facets of the variable.
        branded_var = "_".join(variable.split(".")[1:3])
        freq = variable.split(".")[-2]

        # Identify if the variable is a BCV.
        bcv = TICK if check_if_bcv(variable) is True else CROSS

        # Filter the ESGF archive to get data for only the current variable.
        filtered_esgf = filter_esgf_archive(branded_var)
        # Identify which models the variable is theoretically producible with.
        models = search_available_models(branded_var, freq)
        for model in models:
            known_issue = ISSUE if check_if_known_issue(variable, model) is True else ""
            match_count = 0
            for member in filtered_esgf:
                # Itterate through all data so that different variants of the same experiment can be picked up.
                if member.get("var") == branded_var and member.get("freq") == freq and member.get("model") == model:
                    # Identify if the variable is in the known issues.
                    table_data.append([f"{branded_var}@{freq}{known_issue}", bcv, member.get("model"), TICK,
                                       member.get("exp"), member.get("variant"), member.get("start"),
                                       member.get("end")])
                    match_count += 1
            # If no match is found, add a template row to show that the data has not yet been published for this model.
            if match_count == 0:
                table_data.append([f"{branded_var}@{freq}{known_issue}", bcv, model, CROSS, "-", "-", "-", "-"])

    table_data = [HEADINGS] + table_data

    return table_data


def build_table(table_data: list[list]) -> str:
    """Build the HTML for table showing the supplied table_data

    Parameters
    ----------
    table_data : list[list])
        The data to populate the table with.

    Returns
    -------
    str
        The table_data formatted as a HTML table.
    """
    print("Building HTML table...")
    html = ''
    for i, row in enumerate(table_data):
        cell_type = 'th' if i == 0 else 'td'
        row_html = ''
        filter_row_html = ''
        # Handle the headers
        if i == 0:
            for entry in row:
                row_html += CELL_TEMPLATE.format(cell_type, "Azure", entry)
                filter_row_html += CELL_TEMPLATE.format(cell_type, "Azure", '')
            html += HEADER_ROW_TEMPLATE.format(BGCOLORS[i % len(BGCOLORS)], row_html, filter_row_html)
            continue
        else:
            variable = row[0].split("_")[0]
            for entry in row:
                if entry == table_data[i][0]:
                    row_html += CELL_TEMPLATE.format(cell_type, "Azure",
                                                     HYPERLINK.format(CLIMATE_RESOURCE_LINK.format(variable), entry))
                else:
                    row_html += CELL_TEMPLATE.format(cell_type, "Azure", entry)

            html += ROW_TEMPLATE.format(BGCOLORS[i % len(BGCOLORS)], row_html)

    table_html = TABLE_TEMPLATE.format(html)

    return table_html


def generate_html(table_html: str) -> None:
    """Generates full HTML file.

    Parameters
    ----------
    table_html : str
        The HTML table.
    """
    print("Building full HTML...")
    html = (HEADER +
            '<p style="text-align: right;"><a href="https://github.com/UKNCSP/CDDS-simulation-metadata">'
            'Back to CDDS-simulation-metadata  </a></p>' +
            f'<p style="text-align: right;"> Last Updated: {LAST_UPDATED} </p>' +
            '<h2>CMIP7 Global Climate Variables</h2>' +
            '<p> </p>' + '<p>Use the search box to filter rows.</p>' + '<p> </p>' +
            '<p>To view the ESGF climate information, click the variable name link in the table. Please note that '
            f'variables marked with {ISSUE}, may have a known issue assocaited with one or more experiments for the '
            'model listed. Please visit the <a href='
            '"https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/reference_information/known_issues.json"> '
            'known issue dictionary </a> for more information.</p>' +
            table_html + FOOTER)

    output_directory = Path("docs/variable_information")
    output_directory.mkdir(parents=True, exist_ok=True)

    output_filepath = output_directory / "publication_table.html"

    with open(output_filepath, 'w', encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    generate_html(build_table(generate_table_data()))
