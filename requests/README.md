## Getting Your Request File Running
To run your request file it is important that you download the request file and its corresponding variable list to within your $HOME directory BEFORE you make any changes. These files do not need to be in the same location, however it is often helpful to keep them together. 

Please DO NOT make any changes to the request file on the repository itself.

Once the request file and corresponding variable list file are in your $HOME space, you will need to update the path under 'variable_list_file' in the request in the section 'data'.

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

For additional advice on common errors that you may encounter, please visit the [wiki](https://github.com/UKNCSP/CDDS-simulation-metadata/wiki) or contact a member of the CDDS team for support.