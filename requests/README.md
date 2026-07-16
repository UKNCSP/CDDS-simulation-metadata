> **IMPORTANT:
>  Do not edit any request or variable list files directly within the repository. To make any changes, you must first download it and only make edits to your local copy.**

## Finding Your Request
> **NOTE:
>  In order to generate a request file, please navigate to the github issues page and fill out the issue form titled `Request The Generation Of A CDDS Request File`. You will need to know the model workflow ID that you would like to generate a request for, the type of request you would like (a standard Met Office request (default) or a JASMIN based request), the streams you would like to process with and a package name (used to distinguish between different runs using the same model workflow ID).

The name of your request file will be noted in the comments of the issue that was opened upon filling out the `Request The Generation Of A CDDS Request File` issue form. Please be aware that this issue is likely to have been closed. Alternatively, you can easily identify your request file as the file that contains the model workflow ID and package name given in the `Request The Generation Of A CDDS Request File` issue form. Do not edit any request or variable list files directly within the repository. To make any changes, you must first download it and only make edits to your local copy.


## Getting Your Request Running
To run your request file it is important that you download the request file and its corresponding variable list to within your $HOME directory BEFORE you make any changes. These files do not need to be in the same location, however it is often helpful to keep them together. 

Please DO NOT make any changes to the request file on the repository itself.

Once the request file and corresponding variable list file are in your $HOME space, you will need to update the path under 'variable_list_file' in the request in the 'data' section. For those with a JASMIN request. You will also need to populate the 'jasmin_account' entry in the 'conversion' section.

1. Activate the CDDS environment by giving the following command in the terminal:
    ```bash
    source ~cdds/bin/setup_env_for_cdds <the version of CDDS you are using, e.g. 3.4.0>
    ```

2. Create the directory structure. This is where the logs and data files are stored during and after processing
    ```bash
    create_cdds_directory_structure request.cfg
    ```

3. Create the internal variable list file. This is used by CDDS during processing
    ```bash
    prepare_generate_variable_list request.cfg
    ```

4. Run the conversion workflow. This generates mip convert template files, copies the conversion workflow, populates Jinja2 template variables and submits a cylc workflow using `cylc vip .`. This cylc workflow can be monitored and viewed in the usual way on cylc Hub or cylc review. This workflow should appear running under the name 'cdds_<model>_<experiment>_<variant_label>'
    ```bash
    cdds_convert request.cfg
    ```

For additional advice on common errors that you may encounter, please visit the [wiki](https://github.com/UKNCSP/CDDS-simulation-metadata/wiki) or contact a member of the CDDS team for support. You can also find operational procedure documentation for CMIP7 through the main CDDS repository [here](https://metoffice.github.io/CDDS/latest/operational_procedure/).
