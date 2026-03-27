# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""A script to generate a functional request file using information provided from a given workflow metadata
configuration file.

Example command line usage:
python scripts/generate_request.py a-bc123
"""
import argparse
import datetime

from configparser import ConfigParser, SectionProxy

WORKFLOW_METADATA_DIR = "workflow_metadata"
VARIABLE_LIST_DIR = "variables/v1.2.2.3"
REQUEST_TEMPLATE = {
    "metadata": {
        "base_date": "",
        "branch_method": "",
        "calendar": "",
        "experiment_id": "",
        "institution_id": "",
        "license": "CC-BY-4.0",
        "mip": "",
        "mip_era": "",
        "model_id": "",
        "variant_label": "",
        "branch_date_in_child": "",
        "branch_date_in_parent": "",
        "parent_experiment_id": "",
        "parent_mip": "",
        "parent_mip_era": "",
        "parent_model_id": "",
        "parent_time_units": "",
        "parent_variant_label": "",
    },
    "netcdf_global_attributes": {
        "data_specs_version": "MIP-DS7.1.0.0",
        "drs_specs": "MIP-DRS7",
        "region": "glb"
    },
    "common": {
        "external_plugin": "",
        "external_plugin_location": "",
        "log_level": "INFO",
        "mip_table_dir": "$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.3-v1.0.2",
        "mode": "strict",
        "package": "",
        "root_ancil_dir": "$CDDS_ETC/ancil_testing/",
        "root_hybrid_heights_dir": "$CDDS_ETC/vertical_coordinates/",
        "root_replacement_coordinates_dir": "$CDDS_ETC/horizontal_coordinates/",
        "root_proc_dir": "$CDDS_DATA/proc",
        "root_data_dir": "$CDDS_DATA/data",
        "sites_file": "$CDDS_ETC/cfmip2/cfmip2-sites-orog.txt",
        "standard_names_dir": "$CDDS_ETC/standard_names/",
        "standard_names_version": "latest",
        "workflow_basename": ""
    },
    "data": {
        "end_date": "",
        "mass_data_class": "",
        "mass_ensemble_member": "",
        "model_workflow_id": "",
        "output_mass_suffix": "production",
        "output_mass_root": "moose:/adhoc/projects/cdds",
        "start_date": "",
        "streams": "ap4 ap5 ap6 ap7 ap8 ap9 apu apt inm onm ind ond",
        "variable_list_file": ""
    },
    "misc": {
        "atmos_timestep": ""
    },
    "conversion": {
        "continue_if_mip_convert_failed": "False",
        "cylc_args": "-v",
        "mip_convert_plugin": "",
        "skip_extract": "False",
        "skip_extract_validation": "False",
        "skip_configure": "False",
        "skip_qc": "False",
        "skip_archive": "False"
    }
}


def arg_parser() -> argparse.Namespace:
    """Creates an argument parser to take user inputs from the command line.

    Returns
    -------
    argparse.Namespace
        The argument parser to handle source file paths.
    """
    parser = argparse.ArgumentParser(description="Generates a usable request file from a given metadata issue form")

    parser.add_argument("model_workflow_id", help="The model workflow id of the form u-ab123")

    return parser.parse_args()


def identify_mip_convert_plugin(metadata: SectionProxy) -> str:
    """Identifies the relevant MIP convert plugin using the model id given in the workflow metadata configuration file.

    Parameters
    ----------
    metadata: SectionProxy
        The metadata section of the workflow metadata configuration file.

    Returns
    -------
    str
        The MIP convert plugin.

    Raises
    ------
    RuntimeError
        If a valid plugin cannot be identified from the given model_id.
    """
    model = metadata["model_id"]
    if model in ["UKCM2-0-LL", "UKCM2a-0-HH"]:
        return "UKCM2"
    elif model == "UKESM1-3-LL":
        return "UKESM1p3"
    elif model == "HadGEM3-GC31-MM":
        return "HadGEM3"
    else:
        raise RuntimeError(f"Unable to map model {model} to a valid plugin")


def update_template_with_metadata(request: dict, metadata: SectionProxy) -> dict:
    """Populates the REQUEST_TEMPLATE with the metadata information given in the workflow metadata configuration file.

    Parameters
    ----------
    request: dict
        The request template fields and values as a dictionary.
    metadata: SectionProxy
        The metadata section of the workflow metadata configuration file.

    Returns
    -------
    dict
        The request template with a populated metadata section.
    """
    for key in request["metadata"]:
        if key in metadata:
            request["metadata"][key] = metadata[key]

    if request["metadata"]["calendar"] == "gregorian":
        request["metadata"]["calendar"] = "standard"

    return request


def update_template_with_data(request: dict, data: SectionProxy, metadata: SectionProxy) -> dict:
    """Populates the REQUEST_TEMPLATE with the data information given in the workflow metadata configuration file.

    Parameters
    ----------
    request: dict
        The request template fields and values as a dictionary.
    data: SectionProxy
        The data section of the workflow metadata configuration file.
     metadata: SectionProxy
        The metadata section of the workflow metadata configuration file.

    Returns
    -------
    dict
        The request template with a populated data section.
    """
    for key in request["data"]:
        if key in data:
            request["data"][key] = data[key]

    var_file = f"{VARIABLE_LIST_DIR}/{data['model_workflow_id']}_{metadata['experiment_id']}_{metadata['model_id']}.txt"
    request["data"]["variable_list_file"] = var_file

    return request


def update_template_with_misc(request: dict, misc: SectionProxy) -> dict:
    """Populates the REQUEST_TEMPLATE with the misc information given in the workflow metadata configuration file.

    Parameters
    ----------
    request: dict
        The request template fields and values as a dictionary.
    misc: SectionProxy
        The misc section of the workflow metadata configuration file.

    Returns
    -------
    dict
        The request template with a populated misc section.
    """
    for key in request["misc"]:
        if key in misc:
            request["misc"][key] = misc[key]

    return request


def update_template_with_common(request: dict, metadata: SectionProxy) -> dict:
    """Populates the REQUEST_TEMPLATE with the common information generated using information provided in the workflow
    metadata configuration file.

    Parameters
    ----------
    request: dict
        The request template fields and values as a dictionary.
    metadata: SectionProxy
        The metadata section of the workflow metadata configuration file.

    Returns
    -------
    dict
        The request template with a populated common section.
    """
    request_common = request["common"]
    basename = f"{metadata['model_id']}_{metadata['experiment_id']}_{metadata['variant_label']}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    request_common["workflow_basename"] = basename
    request_common["package"] = f"round_{timestamp}"

    return request


def update_template_with_conversion(request: dict, metadata: SectionProxy) -> dict:
    """Populates the REQUEST_TEMPLATE with the conversion information generated using information provided in the
    workflow metadata configuration file.

    Parameters
    ----------
    request: dict
        The request template fields and values as a dictionary.
    metadata: SectionProxy
        The metadata section of the workflow metadata configuration file.

    Returns
    -------
    dict
        The request template with a populated conversion section.
    """
    request["conversion"]["mip_convert_plugin"] = identify_mip_convert_plugin(metadata)

    return request


def write_request(data: SectionProxy, request: dict) -> None:
    """Writes out the fully populated REQUEST TEMPLATE dictionary to a configuration file format.

    Parameters
    ----------
    data: SectionProxy
        The data section of the workflow metadata configuration file.
    request: dict
        The fully populated request template fields and values as a dictionary.
    """
    filename = f"request_{data['model_workflow_id']}_{request['common']['package']}.cfg"
    with open(filename, "w") as f:
        for section_header, content in request.items():
            f.write(f"[{section_header}]\n")
            if isinstance(content, dict):
                for parameter, value in content.items():
                    f.write(f"{parameter} = {value}\n")
                f.write("\n")


def generate_request_config() -> None:
    """Generates a functional request file using the information given in the workflow metadata issue form."""
    args = arg_parser()
    request = REQUEST_TEMPLATE

    cfg_file = f"{WORKFLOW_METADATA_DIR}/{args.model_workflow_id}.cfg"
    config = ConfigParser()
    config.read(cfg_file)

    metadata = config["metadata"]
    data = config["data"]
    misc = config["misc"]

    update_template_with_metadata(request, metadata)
    update_template_with_data(request, data, metadata)
    update_template_with_misc(request, misc)
    update_template_with_common(request, metadata)
    update_template_with_conversion(request, metadata)

    write_request(data, request)


if __name__ == "__main__":
    generate_request_config()
