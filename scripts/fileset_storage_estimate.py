# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Generates estimated storage requirements in TB for each file in `workflow_metadata/*cfg` and applies some manual
overrides."""

from metadata_config_tools import MetadataConfigTools
from constants import WORKFLOW_METADATA_DIR, FILESET_ESTIMATES_DIR

MAXIMUM_EST = 80
GB_TO_TB = 1e-3  # 1GB = 0.001TB
MANUAL_ESTIMATES_PATH = FILESET_ESTIMATES_DIR / "manual_updates.txt"
MODEL_DEFAULT_SIZE_GB_PER_YEAR = {
    "UKCM2-0-LL": 24,
    "UKCM2a-0-HH": 1400,
    "UKESM1-3-LL": 40
}
OVERRIDES_GB_PER_YEAR = {
    "UKCM2a-0-HH/piControl": 480,
    "UKCM2-0-LL/piControl": 7,
    "UKESM1-3-LL/esm-piControl": 10,
    "UKCM2a-0-HH/amip": 186
}


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
    gb_per_year = OVERRIDES_GB_PER_YEAR.get(f"{metadata._model_id}/{metadata._experiment_id}",
                                            MODEL_DEFAULT_SIZE_GB_PER_YEAR.get(metadata._model_id))

    # Round to the nearest decimal place since this is an estimate.
    return round(gb_per_year * metadata._run_length_years * GB_TO_TB, 1)


def check_for_hand_edits(hand_edits: list, path: str) -> bool:
    """Checks if a single workflow has entries in the HAND_EDITS list that need to be highlighted.

    Parameters
    ----------
    hand_edits: list
        The content of `MANUAL_ESTIMATES_PATH` as a list if lines.
    path: str
        The DRS path structure for the workflow being checked.

    Returns
    -------
    bool
        `True` if the workflow has an entry in HAND_EDITS, `False` if not.
    """
    for line in hand_edits:
        if "/".join(path.split("/")[:-1]) in line:
            return True

    return False


def write_estimates_to_file(hand_edits: list, generated_estimates: list) -> None:
    """Writes out the fileset storeage estimate to a txt file.

    Parameters
    ----------
    hand_edits: list
        The content of `MANUAL_ESTIMATES_PATH` as a list if lines.
    generated_estimate: list
        A list of DRS path structure for each workflow and its correspondind estimated storage requirement in TB.
    """
    with open("fileset_storage_estimates/fileset_estimates.txt", "w") as f:
        for item in hand_edits:
            f.write(item)
        for item in sorted(generated_estimates):
            f.write(item)


def main() -> None:
    """Main."""
    generated_estimates = ["\n\n# Auto generated estimations from metadata\n"]
    with open(MANUAL_ESTIMATES_PATH, "r") as f:
        hand_edits = f.readlines()

    all_metadata_configs = list(WORKFLOW_METADATA_DIR.glob('*.cfg'))
    for file in all_metadata_configs:
        # Pull the workflow ID from the filename so that MetadataConfigTools knows which metadata file to read.
        workflow_id = str(file).split("/")[-1].strip(".cfg")
        metadata = MetadataConfigTools(workflow_id)
        metadata.read_config()

        size_est = calc_size_estimate(metadata)
        path = (f"{metadata._drs_specs}/{metadata._mip_era}/{metadata._mip}/{metadata._institution_id}/"
                f"{metadata._model_id}/{metadata._experiment_id}/{metadata._variant_label}")

        # If the path does not appear in `MANUAL_ESTIMATES_PATH`, add it to the list of generated estimates.
        if check_for_hand_edits(hand_edits, path) is False:
            if size_est > MAXIMUM_EST:
                generated_estimates.append(
                    f"# !!! Fileset estimate for {path} exceeds {MAXIMUM_EST}TB (estimate={size_est}TB), please create "
                    f"manual estimate in {MANUAL_ESTIMATES_PATH}"
                )
            else:
                generated_estimates.append(f"{path} {size_est}\n")

    write_estimates_to_file(hand_edits, generated_estimates)


if __name__ == "__main__":
    main()
