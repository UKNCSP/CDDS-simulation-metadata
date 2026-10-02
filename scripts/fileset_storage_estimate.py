# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Generates estimated storage requirements in TB for each file in `workflow_metadata/*cfg` and applies some manual
overrides."""

from metadata_config_tools import MetadataConfigTools
from constants import WORKFLOW_METADATA_DIR

GB_TO_TB = 1e-3  # 1GB = 0.001TB
MODEL_DEFAULT_SIZE_GB_PER_YEAR = {
    "UKCM2-0-LL": 24,
    "UKCM2a-0-HH": 40,
    "UKESM1-3-LL": 1400
}
OVERRIDES_GB_PER_YEAR = {
    "UKCM2a-0-HH/piControl": 480,
    "UKCM2-0-LL/piControl": 7,
    "UKESM1-3-LL/esm-piControl": 10,
    "UKCM2a-0-HH/amip": 186
}
HAND_EDITS = [
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/mon 55.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/day 35.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/mon 48.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/day 32.0\n"
]


def calc_size_estimate(metadata: MetadataConfigTools) -> float:
    """Estimates the storage requirements for a given workflow in TB using its run length in years.

    Parameters
    ----------
    metadata: MetadataConfigTools
        The config object for a single workflow metadata file.

    Returns
    -------
    float
        Estiamted storage needs for a single workflow to in TB 1dp.
    """
    if f"{metadata._model_id}/{metadata._experiment_id}" in OVERRIDES_GB_PER_YEAR:
        gb_per_year = OVERRIDES_GB_PER_YEAR.get(f"{metadata._model_id}/{metadata._experiment_id}")
    else:
        # If there are no matching overrides, use default values.
        gb_per_year = MODEL_DEFAULT_SIZE_GB_PER_YEAR.get(metadata._model_id)

    # Round to the nearest decimal place since this is an estimate.
    return round(gb_per_year * metadata._run_length_years * GB_TO_TB, 1)


def check_for_hand_edits(path: str) -> bool:
    """Checks if a single workflow has entries in the HAND_EDITS list that need to be highlighted.

    Parameters
    ----------
    path: str
        The DRS path structure for the workflow being checked.

    Returns
    -------
    bool
        `True` if the workflow has an entry in HAND_EDITS, `False` if not.
    """
    for line in HAND_EDITS:
        if "/".join(path.split("/")[:-1]) in line:
            return True

    return False


def write_estimates_to_file(generated_estimates) -> None:
    """Writes out the fileset storeage estimate to a txt file.

    Parameters
    ----------
    generated_estimate: list
        A list of DRS path structure for each workflow and its correspondind estimated storage requirement in TB.
    """
    hand_edits = ["# CMIP7 Fileset estimated storage requirements in TB\n", "# Specific hand-edits\n"] + HAND_EDITS
    with open("fileset_storage_estimates/fileset_estimates.txt", "w") as f:
        for item in hand_edits:
            f.write(item)
        for item in sorted(generated_estimates):
            f.write(item)


def main() -> None:
    """Main."""
    generated_estimates = ["\n# Auto generated estimations from metadata\n"]

    all_metadata_configs = list(WORKFLOW_METADATA_DIR.glob('*.cfg'))
    for file in all_metadata_configs:
        workflow_id = str(file).split("/")[-1].strip(".cfg")
        metadata = MetadataConfigTools(workflow_id)
        metadata.read_config()
        size_est = calc_size_estimate(metadata)
        path = f"MIP-DRS7/CMIP7/CMIP/UKNCSP/{metadata._model_id}/{metadata._experiment_id}/{metadata._variant_label}"
        if check_for_hand_edits(path) is True:
            generated_estimates.append(f"{path} {size_est} # PLEASE CHECK HAND_EDITS SECTION FOR DETAILS\n")
        else:
            generated_estimates.append(f"{path} {size_est}\n")

    write_estimates_to_file(generated_estimates)


if __name__ == "__main__":
    main()
