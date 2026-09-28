# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Audits all BCV variables to determine their production status and which experiments they are available in. This
information is then formatted and used to `update bcv_info.html`.
"""

import requests

from pathlib import Path

from common import read_json
from constants import (MAPPINGS_FILE_LOCATION, HEADER_ROW_TEMPLATE, ROW_TEMPLATE, CELL_TEMPLATE,
                       TABLE_TEMPLATE, BGCOLORS, HEADER, FOOTER, HYPERLINK, LAST_UPDATED)

CLIMATE_RESOURCE_LINK = "https://www.climate-resource.com/tools/esm-model/cmip7-availability/variables/{}"
HEADINGS = ["Variable", "Data Available (UKCM2-0-LL)", "Approved (UKCM2-0-LL)", "Published (UKCM2-0-LL)",
            "Data Available (UKCM2a-0-HH)", "Approved (UKCM2a-0-HH)", "Published (UKCM2a-0-HH)",
            "Data Available (UKESM1-3-LL)", "Approved (UKESM1-3-LL)", "Published (UKESM1-3-LL)"]


def get_data_availability(labels, model):
    """Returns `True` if has diagnostic review data available for a given model."""
    if "diagnostic_review_data_available" in labels:
        return True
    if f"diagnostic_review_data_available_OI_{model}" in labels:
        return True

    return False


def get_approval_status(labels, model):
    """Returns `True` is a variable has been approved for production for a given model."""
    if "diagnostic_review_ok" in labels:
        return True
    if f"diagnostic_review_data_ok_OI_{model}" in labels:
        return True

    return False


def get_publication_status(result, full_model_name):
    """Returns `True` if a variable has data published on CEDA for a given model."""
    if "Not yet published by" not in result:
        return False
    if full_model_name in result.split("Not yet published by")[1].split("</div>")[0]:
        return False
    return True


def generate_table_data(bcvs):
    table_data = []
    i = 0
    for i, variable in enumerate(bcvs):
        table_data.append([
            variable,
            bcvs[variable]["UKCM2-0-LL"]["data_available"],
            bcvs[variable]["UKCM2-0-LL"]["approved"],
            bcvs[variable]["UKCM2-0-LL"]["published"],
            bcvs[variable]["UKCM2a-0-HH"]["data_available"],
            bcvs[variable]["UKCM2a-0-HH"]["approved"],
            bcvs[variable]["UKCM2a-0-HH"]["published"],
            bcvs[variable]["UKESM1-3-LL"]["data_available"],
            bcvs[variable]["UKESM1-3-LL"]["approved"],
            bcvs[variable]["UKESM1-3-LL"]["published"],
        ])

    table_data = [HEADINGS] + table_data

    return table_data


def build_table(table_data: list[list[str]]) -> str:
    """Build the HTML for table showing the supplied table_data

    Parameters
    ----------
    table_data : list[list[str]])
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
            variable = row[0]
            for entry in row:
                if entry == table_data[i][0]:
                    row_html += CELL_TEMPLATE.format(cell_type, "Azure",
                                                     HYPERLINK.format(CLIMATE_RESOURCE_LINK.format(variable), entry))
                else:
                    colour = "LightGreen" if entry is True else "Azure"
                    row_html += CELL_TEMPLATE.format(cell_type, colour, entry)

            html += ROW_TEMPLATE.format(BGCOLORS[i % len(BGCOLORS)], row_html)

    table_html = TABLE_TEMPLATE.format(html)
    print("SUCCESSFUL...")

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
            '<h2>CMIP7 Baseline Climate Variables</h2>' +
            '<p> </p>' + '<p>Use the search box to filter rows.</p>' + '<p> </p>' +
            '<p>To view the ESGF climate information, click the variable name link in the table.</p>' +
            table_html + FOOTER)

    output_directory = Path("docs")
    output_directory.mkdir(parents=True, exist_ok=True)

    output_filepath = output_directory / "bcvs_table.html"

    with open(output_filepath, 'w') as f:
        f.write(html)


def main():
    """Main."""
    mappings = read_json(MAPPINGS_FILE_LOCATION)
    bcvs = {}

    for mapping in mappings:
        labels = mapping.get("labels")
        if "do-not-produce" in labels:
            continue
        if "BCV" in labels:
            variable = mapping.get("branded_variable")
            print(f"Processing {variable}")
            bcvs.update({variable: {}})
            ceda_var_site = requests.get(CLIMATE_RESOURCE_LINK.format(variable.split(".")[1])).text
            for model in ("UKCM2-0-LL", "UKCM2a-0-HH", "UKESM1-3-LL"):
                published = get_publication_status(ceda_var_site, model)
                shortened_model = "UKCM2" if model in ("UKCM2-0-LL", "UKCM2a-0-HH") else "UKESM"
                approved = get_approval_status(labels, shortened_model)
                data_available = get_data_availability(labels, shortened_model)
                bcvs[variable].update({model: {}})
                bcvs[variable][model] = {
                            "published": published,
                            "approved": approved,
                            "data_available": data_available
                            }

    generate_html(build_table(generate_table_data(bcvs)))


if __name__ == "__main__":
    main()
