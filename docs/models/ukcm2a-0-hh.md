<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.-->
To update the information on this page please open a branch to edit the [UKCM2a-0-HH pages](https://github.com/UKNCSP/CDDS-simulation-metadata/blob/main/docs/models/ukcm2a-0-hh.md)

# UKCM2a-0-HH
UKCM2a-0-HH is a very-high resolution model using an N640 atmosphere grid (20 km in mid latitudes, 31 km at the equator) and a 1/12 degree (8 km) extended ORCA ocean grid. UKCM2a-HH and [UKCM2-0-LL](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-1676/) share the same underlying science configuration (Xavier et al., 2026)[https://egusphere.copernicus.org/preprints/2026/egusphere-2026-4281/], but UKCM2a-HH uses the CoMorphA9 atmospheric convection scheme [Lock et al., 2023](https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4781) and has various other parameter and resolution-dependent differences.

## Experiments
Due to the expense, UKCM2a-0-HH only contributes to a subset of the CMIP7 AFT simulations. At present we only plan to produce two future scenarios, scen7-h and scen7-vl.

| Experiment name | No. years | Final ensemble size (ambition) |
| ----- | ----- | ----- |
| piControl | 500 | 1 |
| historical | 1850-2021 | 5 |
| scen7-h | 2022-2100 | 5 |
| scen7-vl | 2022-2100  | 5 |
| AMIP |  | 1979-2022 | 2 |
| AMIP+4k | 1979-2022 | 1 |
| abrupt4xCO2 | 150 | 1 |
| 1pcCO2 | 150 | 1 |
| piClim-control | 30 | 1 |
| piClim-aer | 30 | 1 |

## Ensemble Members
Initial historical ensemble member realisations (r1i1p1f1, r2i1p1f1, r3i1p1f1) are initialised from, respectively, the start, year 50 and year 100 of the piControl. Future scenarios use the same realisation numbers and are hence continuous with the historical runs. Members with f2 use the same initial conditions, but have a fix for the LandUse (see Known Limitations).

## Known Limitations
Initial ensemble members (with rip code "f1" within "r1i1p1f1") in experiments that use time-varying forcings (historical, scenarios) have an error in the LandUse component. The LandUse or vegetation fraction (e.g. distribution of trees, grasses, soil etc across model grid points) is not updated year-by-year as it should be, and hence is fixed to the start year of that simulation (1850 for historical and 2022 for scenarios). As expected, this causes regional errors in surface fluxes, temperatures etc (particularly across North America and Northern Europe, but elsewhere too), but analysis so far suggests more limited impacts on global aspects of the circulation.
Further ensemble members (with rip code f2) are being run with this error fixed, and once complete the impacts of this error will become clearer.

## General User Guidance