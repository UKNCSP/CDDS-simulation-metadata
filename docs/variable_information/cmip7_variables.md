<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.-->
# CMIP7 Climate Variables

## The CMIP7 Data Request Structure
After taking on feedback from CMIP6, the data request task team have devised a controlled list of high priority
variables that faciliate the majority of user needs. This structure includes 3 main parts:

1. **Core**- These are the baseline climate variables (BCVs). They are requested as standard across all of CMIP7, ideally produced for all models and experiments to form a base.

2. **Harmonised**- These are high priority variables that faciliate the majority of user needs whilst keeping the data request as managable as possible. This consists of variables across 5 thematic areas: ocean & sea-ice, land & land-ice, atmosphere, Earth system, and impacts & adaptation.

3. **Unharmonised**- This stage allows for MIPs and community activities to exploit the data request without the deadline and engagment restrictions present in the harmonised stage.


## The CMIP7 Variable Name Structure
The way that CMIP7 variable names are written has changed notably since CMIP6: the key aim being to provide more immediate information about the variable.

For example, what was `Amon.tas` in CMIP6 is now written as `tas_tavg-h2m-hxy-u` in CMIP7 (known as a 'branded variable name'). The new structure can be explained as follows:

- **The variable** ID (e.g. `tas`): this identifies the physical quantity and remains unchanged from CMIP6.

- **The temporal label** (e.g. `tavg`): this identifies how the variable is sampled in the time domain.

- **The vertical label** (e.g. `h2m`): this identifies how the variable is sampled in the vertical domain.

- **The horizontal label** (e.g. `hxy`): this identifies how the variable is sampled horizontally. Note that this does **not** denote a particular choice of reporting grid.

- **The area label** (e.g. `u`): this identifies the masked area type for which data is reported where `u` means that no masking is applied (`unmasked`).


Please see the [CMIP7 Guidance Docs](https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Branded_Variables/) for more information.



