# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.

import argparse

from configparser import ConfigParser

WORKFLOW_METADATA_DIR = "workflow_metadata"
VARIABLE_LIST_DIR = "variables/v1.2.2.3"
REQUEST_TEMPLATE = {
    "metadata": {
        "base_date": "",
        "branch_method": "",
        "calendar": "",
        "experiment_id": "",
        "institution_id": "",
        "license": "CC-BY-4-0",
        "mip": "",
        "mip_era": "",
        "model_id": "",
        "model_type": "",
        "variant_label": ""
    },
    "netcdf_global_attributes": {
        "data_specs_version": "MIP-DS7.0.0.0",
        "drs_specs": "MIP-DRS7",
        "host_collection": "CMIP7",
        "region": "glb"
    },
    "common": {
        "external_plugin": "",
        "external_plugin_location": "",
        "log_level": "INFO",
        "mip_table_dir": "$CDDS_ETC/mip_tables/CMIP7/DR-1.2.2.3-v1.0.2",
        "mode": "strict",
        "package": "round-1",
        "root_ancil_dir": "$CDDS_ETC/ancil_testing/",
        "root_hybrid_heights_dir": "$CDDS_ETC/vertical_coordinates/",
        "root_replacement_coordinates_dir": "$CDDS_ETC/horizontal_coordinates/",
        "root_proc_dir": "$DATADIR/cdds_CMIP7/proc",
        "root_data_dir": "$DATADIR/cdds_CMIP7/data",
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
        "output_mass_suffix": "cdds_cmip7",
        "output_mass_root": "moose:/adhoc/users/<moose user id>",
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


def generate_workflow_basename(metadata):

    return f"{metadata["model_id"]}_{metadata["experiment_id"]}_{metadata["variant_label"]}"


def identify_variable_list_file(data, metadata):

    return f"{VARIABLE_LIST_DIR}/{data["model_workflow_id"]}_{metadata["experiment_id"]}_{metadata["model_id"]}.txt"


def identify_mip_convert_plugin(metadata):
    model = metadata["model_id"]
    if model in ["UKCM2-0-LL", "UKCM2a-0-HH"]:
        return "UKCM2"
    elif model == "UKESM1-3-LL":
        return "UKESM1p3"
    elif model == "HadGEM3-GC31-MM":
        return "HadGEM3"
    else:
        raise RuntimeError(f"Unable to map model {model} to a valid plugin")


def update_template_with_metadata(request, metadata):
    for key in request["metadata"]:
        if key in metadata:
            request["metadata"][key] = metadata[key]

    return request


def update_template_with_data(request, data):
    for key in request["data"]:
        if key in data:
            request["data"][key] = data[key]

    return request


def update_template_with_misc(request, misc):
    for key in request["misc"]:
        if key in misc:
            request["misc"][key] = misc[key]

    return request


def write_request(filename, request):
    with open(filename, "w") as f:
        for key, value in request.items():
            f.write(f"[{key}]\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    f.write(f"{k} = {v}\n")
                f.write("\n")


def main():
    args = arg_parser()
    workflow_id = args.model_workflow_id
    cfg_file = f"{WORKFLOW_METADATA_DIR}/{workflow_id}.cfg"
    config = ConfigParser()
    config.read(cfg_file)
    request = REQUEST_TEMPLATE
    metadata = config["metadata"]
    data = config["data"]
    misc = config["misc"]

    update_template_with_metadata(request, metadata)
    update_template_with_data(request, data)
    update_template_with_misc(request, misc)

    request["common"]["workflow_basename"] = generate_workflow_basename(metadata)
    request["data"]["variable_list_file"] = identify_variable_list_file(data, metadata)
    request["conversion"]["mip_convert_plugin"] = identify_mip_convert_plugin(metadata)

    write_request("TEST.cfg", request)


if __name__ == "__main__":
    main()
