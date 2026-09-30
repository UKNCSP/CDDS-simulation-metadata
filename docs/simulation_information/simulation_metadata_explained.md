<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
The metadata for a simulation tells us about things like where the data has come from, how it was processed and the intial conditions that it was derived from. This information stays with any output data throughout its entire lifetime from production to customer, so it is important the metadata is correct and appropriately explains the data that it is attached to. 

## Metadata for simulations with **no** 'parent'
- **Model Workflow ID**- Also sometimes known as the "suite ID". This is a unique identifier used to track an individual workflow. This should generally take the format "u-ab123".
- **Activity ID**- Also sometimes known as the "MIP". This is a standardised, short identifier that specifies which overarching sub-project or MIP (Model Intercomparison Project) that a climate simulation belongs to (e.g. "CMIP").
- **Experiment ID**- The standardised name used to identify a specific experiment. Please note that case is important here (e.g."piControl").
- **Model ID**- Also sometimes known as the "source ID". This is the short name identifying the model used in the workflow (e.g. "UKCM2-0-LL")
- **Variant Label**- This helps us to distinguish between multiple climate simulations run by the same modelling centre and indicates specific changes in how the model was set up or run. This takes the form of a strict regex pattern (r{\d}i{\d}p{\d}f{\d}) so it is important that these are given in the correct order (e.g. "r1i1p1f1"). Each component of the label tells us different things.
    - Realization (r): Distinguishes between those that are identical in physics and forcing but start from different initial conditions.
    - Initialisation (i): Differentiates runs that use different initialisation procedures or data assimilation techniques.
    - Physics (p): Identifies variations in the model parameterisations or physics (e.g. changing cloud physics or atmospheric convection schemes).
    - Forcing (f): Indicates runs that apply different external forcing agents (such as altered greenhouse gas emissions or different aerosol data).
- **Start Date**- The processing start date. This should take the form YYYY-MM-DDThh:mm:ssZ (e.g. "1850-01-01T00:00:00Z").
- **End Date**- The processing end date. This should take the form YYYY-MM-DDThh:mm:ssZ (e.g. "2100-01-01T00:00:00Z").
- **Branch Method**- This tells us whether the workflow uses a parent experiment for any initial conditions or not. If the workflow does use a parent experiment then the branching method is "standard", if not, it is "no parent".
- **Calendar Type**- The type of calendar used in the workflow. This is generally "360_day" or "proleptic_gregorian".
- **Institution ID**- This is used to identify the specific climate modelling centre or research institution that produced a climate dataset. The default for any data produced with CDDS is "UKNCSP". This should always be used unless discussed with the CMIP project team.
- **MIP Era**- This is the era of the model intercomparison project. We expect this to be CMIP7 for all submissions.
- **Atmospheric Timestep**- This is the atmospheric time step used in seconds. This is usually 1800 for N96.
- **Mass Data Class**- This is the root of the location of input dataset on MASS. This is "crum" for most submissions. When using the mass data class of "crum", the **Mass Ensemble Member ID** field should be ignored. However, if using a data class of "ens" a **Mass Ensemble Member ID** is required. If processing on JASMIN, this should be the default "crum".


## Metadata for standard simulations **with** a 'parent'
As well as all of the information noted in the `Metadata for simulations with **no** 'parent'` section. Simulations with the branching method "standard" also requires some additional information. This is because we need to know about the parent that they were initialised from.

- **Child Branch Date**- The date in this simulation where the initial conditions from parent were applied to the experiment for use as a foundation (e.g. "1900-01-01T00:00:00Z").
- **Parent Branch Date**- The date in the parent simulation where the initial conditions were taken from and applied to the experiment for use as a foundation (e.g. "1850-01-01T00:00:00Z").
- **Parent Experiment ID**- The experiment ID for the parent as described in the standard fields section (e.g. "piControl-spinup").
- **Parent Activity ID**- The activity ID for the parent as described in the standard fields section (e.g. "CMIP").
- **Parent MIP Era**- The MIP Era for the parent as described in the standard fields section.
- **Parent Model ID**- The Model ID for the parent as described in the standard fields section. This should match the Model ID given for the experiment (e.g. "UKCM2-0-LL").
- **Parent Time Units**- The time units for the parent experiment. We expect this to be "days since 1850-01-01".
- **Parent Variant Label**- The variant label of the parent as described in the standard fields section (e.g. "r1i1p1f1").