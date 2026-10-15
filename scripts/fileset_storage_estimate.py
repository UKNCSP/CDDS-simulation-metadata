# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
"""Generates estimated storage requirements in TB for each file in `workflow_metadata/*cfg` and applies some manual
overrides."""

from metadata_config_tools import MetadataConfigTools
from constants import WORKFLOW_METADATA_DIR

GB_TO_TB = 1e-3  # 1GB = 0.001TB
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
HAND_EDITS = [
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/mon 55.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/historical/*/glb/day 35.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/mon 48.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/abrupt-4xCO2/*/glb/day 32.0\n",
    "\n",
    "# Various special cases for MIP-DRS7.CMIP7.CMIP.UKNCSP.UKCM2a-0-HH.piControl",
    "\n",
    "# Monthly\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsucs4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsucs 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsu4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsu 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsdcs4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsdcs 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsd4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rsd 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rlucs4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rlucs 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rlu4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rlu 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rldcs4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rldcs 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rld4co2 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/rld 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mcu 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mcd 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mc 1.04\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/hur 1.07\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mmrso4 1.13\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mmroa 1.14\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mmrbc 1.15\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mmrdust 1.16\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/mmrss 1.18\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/so2 1.19\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/dms 1.26\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/bigthetao 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/masscello 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/so 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/thetao 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/thkcello 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/umo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/uo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/vmo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/vo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/wmo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/wo 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/agessc 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/ficeberg 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon/obvfsq 11.50\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/mon 74.0\n",
    "# daily\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/sos 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/tos 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/zos 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/mlotst 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/tossq 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/uos 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/vos 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/t20d 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/siconc 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/sithick 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/sitimefrac 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/siu 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/siv 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/snd 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/bigthetao 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/thetao 4.66\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/ua 4.83\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/va 4.95\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/ta 5.20\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/hus 6.74\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/utendnogw 6.98\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/hur 7.28\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/wap 9.85\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day/pfull 23.76\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/day 38.0\n",
    "# sub daily\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/6hr 74.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/3hr 56.0\n",
    "MIP-DRS7/CMIP7/CMIP/UKNCSP/UKCM2a-0-HH/piControl/r1i1p1f1/glb/1hr 18.0\n",
    "\n",
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
        if check_for_hand_edits(path) is False:
            generated_estimates.append(f"{path} {size_est}\n")

    write_estimates_to_file(generated_estimates)


if __name__ == "__main__":
    main()
