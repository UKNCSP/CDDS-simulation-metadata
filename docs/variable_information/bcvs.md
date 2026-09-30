<!--(C) British Crown Copyright 2026, Met Office. Please see LICENSE.md for license details.--> 
# What are 'Baseline Climate Variables'?
Baseline Climate Variables (otherwise known as 'BCVs') is a core list of scientifically vital variables derived from the most heavily utilized elements of previous cycles.

- **atmos.areacella.ti-u-hxy-u.fx.glb** (fx.areacella): Grid-Cell Area for Atmospheric Grid Variables
Cell areas for any grid used to report atmospheric variables and any other variable using that grid (e.g., soil moisture content). These cell areas should be defined to enable exact calculation of global integrals (e.g., of vertical fluxes of energy at the surface and top of the atmosphere).

- **atmos.cl.tavg-al-hxy-u.mon.glb** (Amon.cl): Percentage Cloud Cover
Includes both large-scale and convective cloud.

- **atmos.cli.tavg-al-hxy-u.mon.glb** (Amon.cli): Mass Fraction of Cloud Ice
Includes both large-scale and convective cloud. This is calculated as the mass of cloud ice in the grid cell divided by the mass of air (including the water in all phases) in the grid cell. It includes precipitating hydrometeors ONLY if the precipitating hydrometeors affect the calculation of radiative transfer in model.

- **atmos.clivi.tavg-u-hxy-u.mon.glb** (Amon.clivi): Ice Water Path
Mass of ice water in the column divided by the area of the column (not just the area of the cloudy portion of the column). Includes precipitating frozen hydrometeors ONLY if the precipitating hydrometeor affects the calculation of radiative transfer in model.

- **atmos.clt.tavg-u-hxy-u.day.glb** (day.clt): Total Cloud Cover Percentage
For the whole atmospheric column, as seen from the surface or the top of the atmosphere. Includes both large-scale and convective cloud.

- **atmos.clt.tavg-u-hxy-u.mon.glb** (Amon.clt): Total Cloud Cover Percentage
For the whole atmospheric column, as seen from the surface or the top of the atmosphere. Include both large-scale and convective cloud.

- **atmos.clw.tavg-al-hxy-u.mon.glb** (Amon.clw): Mass Fraction of Cloud Liquid Water
Includes both large-scale and convective cloud. Calculate as the mass of cloud liquid water in the grid cell divided by the mass of air (including the water in all phases) in the grid cells. Precipitating hydrometeors are included ONLY if the precipitating hydrometeors affect the calculation of radiative transfer in model.

- **atmos.clwvi.tavg-u-hxy-u.mon.glb** (Amon.clwvi): Condensed Water Path
Mass of condensed (liquid + ice) water in the column divided by the area of the column (not just the area of the cloudy portion of the column). Includes precipitating hydrometeors ONLY if the precipitating hydrometeor affects the calculation of radiative transfer in model.

- **atmos.evspsbl.tavg-u-hxy-u.mon.glb** (Amon.evspsbl): Evaporation Including Sublimation and Transpiration
At surface; flux of water into the atmosphere due to conversion of both liquid and solid phases to vapor (from underlying surface and vegetation).

- **atmos.hfls.tavg-u-hxy-u.mon.glb** (Amon.hfls): Surface Upward Latent Heat Flux
Includes both evaporation and sublimation.

- **atmos.hfss.tavg-u-hxy-u.mon.glb** (Amon.hfss): Surface Upward Sensible Heat Flux
The surface sensible heat flux, also called turbulent heat flux, is the exchange of heat between the surface and the air by motion of air.

- **atmos.hur.tavg-p19-hxy-air.mon.glb** (Amon.hur): Relative Humidity
This is the relative humidity with respect to liquid water for T> 0 C, and with respect to ice for T<0 C.

- **atmos.hur.tavg-p19-hxy-u.day.glb** (day.hur): Relative Humidity
This is the relative humidity with respect to liquid water for T> 0 C, and with respect to ice for T<0 C.

- **atmos.hurs.tavg-h2m-hxy-u.6hr.glb** (6hrPlev.hurs): Near-Surface Relative Humidity
The relative humidity with respect to liquid water for T> 0 C, and with respect to ice for T<0 C.

- **atmos.hurs.tavg-h2m-hxy-u.day.glb** (day.hurs): Near-Surface Relative Humidity
This is the relative humidity with respect to liquid water for T> 0 C, and with respect to ice for T<0 C.

- **atmos.hurs.tavg-h2m-hxy-u.mon.glb** (Amon.hurs): Near-Surface Relative Humidity
This is the relative humidity with respect to liquid water for T> 0 C, and with respect to ice for T<0 C.

- **atmos.hus.tavg-p19-hxy-u.day.glb** (day.hus): Specific Humidity
Specific humidity is the mass fraction of water vapor in (moist) air.

- **atmos.hus.tavg-p19-hxy-u.mon.glb** (Amon.hus): Specific Humidity
Specific humidity is the mass fraction of water vapor in (moist) air.

- **atmos.huss.tavg-h2m-hxy-u.day.glb** (day.huss): Near-Surface Specific Humidity
Near-surface (usually, 2 meter) specific humidity.

- **atmos.huss.tavg-h2m-hxy-u.mon.glb** (Amon.huss): Near-Surface Specific Humidity
Near-surface (usually, 2 meter) specific humidity.

- **atmos.huss.tpt-h2m-hxy-u.3hr.glb** (3hr.huss): Near-Surface Specific Humidity
This is sampled synoptically.

- **atmos.pr.tavg-u-hxy-u.1hr.glb** (E1hr.pr): Precipitation
Total precipitation flux.

- **atmos.pr.tavg-u-hxy-u.3hr.glb** (3hr.pr): Precipitation
At surface; includes both liquid and solid phases. This is the 3-hour mean precipitation flux.

- **atmos.pr.tavg-u-hxy-u.day.glb** (day.pr): Precipitation
At surface; includes both liquid and solid phases from all types of clouds (both large-scale and convective).

- **atmos.pr.tavg-u-hxy-u.mon.glb** (Amon.pr): Precipitation
At surface; includes both liquid and solid phases from all types of clouds (both large-scale and convective).

- **atmos.prc.tavg-u-hxy-u.mon.glb** (Amon.prc): Convective Precipitation
At surface; includes both liquid and solid phases.

- **atmos.prsn.tavg-u-hxy-u.mon.glb** (Amon.prsn): Snowfall Flux
At surface; includes precipitation of all forms of water in the solid phase.

- **atmos.prw.tavg-u-hxy-u.mon.glb** (Amon.prw): Water Vapor Path
Vertically integrated mass of water vapour through the atmospheric column.

- **atmos.ps.tavg-u-hxy-u.day.glb** (CFday.ps): Surface Air Pressure
Surface pressure (not mean sea-level pressure), 2-D field to calculate the 3-D pressure field from hybrid coordinates.

- **atmos.ps.tavg-u-hxy-u.mon.glb** (Amon.ps): Surface Air Pressure
Not, in general, the same as mean sea-level pressure.

- **atmos.psl.tavg-u-hxy-u.day.glb** (day.psl): Sea Level Pressure
Sea Level Pressure.

- **atmos.psl.tavg-u-hxy-u.mon.glb** (Amon.psl): Sea Level Pressure
Not, in general, the same as surface pressure.

- **atmos.rlds.tavg-u-hxy-u.mon.glb** (Amon.rlds): Surface Downwelling Longwave Radiation
The surface called "surface" means the lower boundary of the atmosphere. "longwave" means longwave radiation. Downwelling radiation is radiation from above. It does not mean "net downward". When thought of as being incident on a surface, a radiative flux is sometimes called "irradiance". In addition, it is identical with the quantity measured by a cosine-collector light-meter and sometimes called "vector irradiance". In accordance with common usage in geophysical disciplines, "flux" implies per unit area, called "flux density" in physics.

- **atmos.rldscs.tavg-u-hxy-u.mon.glb** (Amon.rldscs): Surface Downwelling Clear-Sky Longwave Radiation
Surface downwelling clear-sky longwave radiation.

- **atmos.rlus.tavg-u-hxy-u.mon.glb** (Amon.rlus): Surface Upwelling Longwave Radiation
The surface called "surface" means the lower boundary of the atmosphere. "longwave" means longwave radiation. Upwelling radiation is radiation from below. It does not mean "net upward". When thought of as being incident on a surface, a radiative flux is sometimes called "irradiance". In addition, it is identical with the quantity measured by a cosine-collector light-meter and sometimes called "vector irradiance". In accordance with common usage in geophysical disciplines, "flux" implies per unit area, called "flux density" in physics.

- **atmos.rluscs.tavg-u-hxy-u.mon.glb** (Amon.rluscs): Surface Upwelling Clear-Sky Longwave Radiation
Surface Upwelling Clear-sky Longwave Radiation.

- **atmos.rlut.tavg-u-hxy-u.mon.glb** (Amon.rlut): TOA Outgoing Longwave Radiation
At the top of the atmosphere (to be compared with satellite measurements).

- **atmos.rlutcs.tavg-u-hxy-u.mon.glb** (Amon.rlutcs): TOA Outgoing Clear-Sky Longwave Radiation
Upwelling clear-sky longwave radiation at top of atmosphere.

- **atmos.rsds.tavg-u-hxy-u.day.glb** (day.rsds): Surface Downwelling Shortwave Radiation
Surface solar irradiance for UV calculations.

- **atmos.rsds.tavg-u-hxy-u.mon.glb** (Amon.rsds): Surface Downwelling Shortwave Radiation
Surface solar irradiance for UV calculations.

- **atmos.rsdscs.tavg-u-hxy-u.mon.glb** (Amon.rsdscs): Surface Downwelling Clear-Sky Shortwave Radiation
Surface solar irradiance clear sky for UV calculations.

- **atmos.rsdt.tavg-u-hxy-u.mon.glb** (Amon.rsdt): TOA Incident Shortwave Radiation
At the top of the atmosphere.

- **atmos.rsus.tavg-u-hxy-u.mon.glb** (Amon.rsus): Surface Upwelling Shortwave Radiation
The surface called "surface" means the lower boundary of the atmosphere. "shortwave" means shortwave radiation. Upwelling radiation is radiation from below. It does not mean "net upward". When thought of as being incident on a surface, a radiative flux is sometimes called "irradiance". In addition, it is identical with the quantity measured by a cosine-collector light-meter and sometimes called "vector irradiance". In accordance with common usage in geophysical disciplines, "flux" implies per unit area, called "flux density" in physics.

- **atmos.rsuscs.tavg-u-hxy-u.mon.glb** (Amon.rsuscs): Surface Upwelling Clear-Sky Shortwave Radiation
Surface Upwelling Clear-sky Shortwave Radiation.

- **atmos.rsut.tavg-u-hxy-u.mon.glb** (Amon.rsut): TOA Outgoing Shortwave Radiation
At the top of the atmosphere.

- **atmos.rsutcs.tavg-u-hxy-u.mon.glb** (Amon.rsutcs): TOA Outgoing Clear-Sky Shortwave Radiation
Calculated in the absence of clouds.

- **atmos.sfcWind.tavg-h10m-hxy-u.day.glb** (day.sfcWind): Near-Surface Wind Speed
Near-surface (usually, 10 meters) wind speed.

- **atmos.sfcWind.tavg-h10m-hxy-u.mon.glb** (Amon.sfcWind): Near-Surface Wind Speed
This is the mean of the speed, not the speed computed from the mean u and v components of wind.

- **atmos.sftlf.ti-u-hxy-u.fx.glb** (fx.sftlf): Percentage of the Grid Cell Occupied by Land (Including Lakes)
Percentage of horizontal area occupied by land.

- **atmos.ta.tavg-p19-hxy-air.day.glb** (day.ta): Air Temperature
Air Temperature.

- **atmos.ta.tavg-p19-hxy-air.mon.glb** (Amon.ta): Air Temperature
Air Temperature.

- **atmos.ta.tpt-p3-hxy-air.6hr.glb** (6hrPlevPt.ta): Air Temperature
Air Temperature.

- **atmos.tas.tavg-h2m-hxy-u.day.glb** (day.tas): Near-Surface Air Temperature
Near-surface (usually, 2 meter) air temperature.

- **atmos.tas.tavg-h2m-hxy-u.mon.glb** (Amon.tas): Near-Surface Air Temperature
Near-surface (usually, 2 meter) air temperature.

- **atmos.tas.tmax-h2m-hxy-u.day.glb** (day.tasmax): Daily Maximum Near-Surface Air Temperature
Maximum near-surface (usually, 2 meter) air temperature (add cell_method attribute "time: max").

- **atmos.tas.tmaxavg-h2m-hxy-u.mon.glb** (Amon.tasmax): Daily Maximum Near-Surface Air Temperature
Monthly mean of the daily-maximum near-surface air temperature.

- **atmos.tas.tmin-h2m-hxy-u.day.glb** (day.tasmin): Daily Minimum Near-Surface Air Temperature
Minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute "time: min").

- **atmos.tas.tminavg-h2m-hxy-u.mon.glb** (Amon.tasmin): Daily Minimum Near-Surface Air Temperature
Monthly mean of the daily-minimum near-surface air temperature.

- **atmos.tas.tpt-h2m-hxy-u.3hr.glb** (3hr.tas): Near-Surface Air Temperature
This is sampled synoptically.

- **atmos.tauu.tavg-u-hxy-u.mon.glb** (Amon.tauu): Surface Downward Eastward Wind Stress
Downward eastward wind stress at the surface.

- **atmos.tauv.tavg-u-hxy-u.mon.glb** (Amon.tauv): Surface Downward Northward Wind Stress
Downward northward wind stress at the surface.

- **atmos.ts.tavg-u-hxy-u.mon.glb** (Amon.ts): Surface Temperature
Surface temperature (skin for open ocean).

- **atmos.ua.tavg-p19-hxy-air.day.glb** (day.ua): Eastward Wind
Zonal wind (positive in a eastward direction).

- **atmos.ua.tavg-p19-hxy-air.mon.glb** (Amon.ua): Eastward Wind
Zonal wind (positive in a eastward direction).

- **atmos.ua.tpt-p3-hxy-air.6hr.glb** (6hrPlevPt.ua): Eastward Wind
Zonal wind (positive in a eastward direction).

- **atmos.uas.tavg-h10m-hxy-u.day.glb** (day.uas): Eastward Near-Surface Wind
Eastward component of the near-surface (usually, 10 meters) wind.

- **atmos.uas.tavg-h10m-hxy-u.mon.glb** (Amon.uas): Eastward Near-Surface Wind
Eastward component of the near-surface (usually, 10 meters) wind.

- **atmos.uas.tpt-h10m-hxy-u.3hr.glb** (3hrPt.uas): Eastward Near-Surface Wind
This is sampled synoptically.

- **atmos.va.tavg-p19-hxy-air.day.glb** (day.va): Northward Wind
Meridional wind (positive in a northward direction).

- **atmos.va.tavg-p19-hxy-air.mon.glb** (Amon.va): Northward Wind
Meridional wind (positive in a northward direction).

- **atmos.va.tpt-p3-hxy-air.6hr.glb** (6hrPlevPt.va): Northward Wind
Meridional wind (positive in a northward direction).

- **atmos.vas.tavg-h10m-hxy-u.day.glb** (day.vas): Northward Near-Surface Wind
Northward component of the near surface wind.

- **atmos.vas.tavg-h10m-hxy-u.mon.glb** (Amon.vas): Northward Near-Surface Wind
Northward component of the near surface wind.

- **atmos.vas.tpt-h10m-hxy-u.3hr.glb** (3hrPt.vas): Northward Near-Surface Wind
This is sampled synoptically.

- **atmos.wap.tavg-p19-hxy-air.mon.glb** (Amon.wap): Omega (=dp/dt)
Commonly referred to as "omega", this represents the vertical component of velocity in pressure coordinates (positive down).

- **atmos.wap.tavg-p19-hxy-u.day.glb** (day.wap): Omega (=dp/dt)
Commonly referred to as "omega", this represents the vertical component of velocity in pressure coordinates (positive down).

- **atmos.zg.tavg-p19-hxy-air.day.glb** (day.zg): Geopotential Height
Geopotential is the sum of the specific gravitational potential energy relative to the geoid and the specific centripetal potential energy. Geopotential height is the geopotential divided by the standard acceleration due to gravity. It is numerically similar to the altitude (or geometric height) and not to the quantity with standard name height, which is relative to the surface.

- **atmos.zg.tavg-p19-hxy-air.mon.glb** (Amon.zg): Geopotential Height
Geopotential is the sum of the specific gravitational potential energy relative to the geoid and the specific centripetal potential energy. Geopotential height is the geopotential divided by the standard acceleration due to gravity. It is numerically similar to the altitude (or geometric height) and not to the quantity with standard name height, which is relative to the surface.

- **land.evspsblsoi.tavg-u-hxy-lnd.mon.glb** (Lmon.evspsblsoi): Water Evaporation from Soil
Includes sublimation.

- **land.evspsblveg.tavg-u-hxy-lnd.mon.glb** (Lmon.evspsblveg): Evaporation from Canopy
The canopy evaporation+sublimation (if present in model).

- **land.lai.tavg-u-hxy-lnd.mon.glb** (Lmon.lai): Leaf Area Index
A ratio obtained by dividing the total upper leaf surface area of vegetation by the (horizontal) surface area of the land on which it grows.

- **land.mrro.tavg-u-hxy-lnd.mon.glb** (Lmon.mrro): Total Runoff
The total runoff (including "drainage" through the base of the soil model) leaving the land portion of the grid cell.

- **land.mrros.tavg-u-hxy-lnd.mon.glb** (Lmon.mrros): Surface Runoff
The total surface runoff leaving the land portion of the grid cell.

- **land.mrso.tavg-u-hxy-lnd.mon.glb** (Lmon.mrso): Total Soil Moisture Content
The mass per unit area (summed over all soil layers) of water in all phases.

- **land.mrsofc.ti-u-hxy-lnd.fx.glb** (fx.mrsofc): Capacity of Soil to Store Water (Field Capacity)
Reported "where land": divide the total water holding capacity of all the soil in the grid cell by the land area in the grid cell; reported as "missing" where the land fraction is 0.

- **land.mrsol.tavg-d10cm-hxy-lnd.mon.glb** (Lmon.mrsos): Moisture in Upper Portion of Soil Column
The mass of water in all phases in a thin surface soil layer.

- **land.orog.ti-u-hxy-u.fx.glb** (fx.orog): Surface Altitude
Height above the geoid; as defined here, "the geoid" is a surface of constant geopotential that, if the ocean were at rest, would coincide with mean sea level. Under this definition, the geoid changes as the mean volume of the ocean changes (e.g., due to glacial melt, or global warming of the ocean). Reported here is the height above the present-day geoid (0.0 over ocean).

- **land.rootd.ti-u-hxy-lnd.fx.glb** (fx.rootd): Maximum Root Depth
Report the maximum soil depth reachable by plant roots (if defined in model), i.e., the maximum soil depth from which they can extract moisture; report as "missing" where the land fraction is 0.

- **land.sftgif.ti-u-hxy-u.fx.glb** (fx.sftgif): Land Ice Area Percentage
Fraction of grid cell occupied by "permanent" ice (i.e., glaciers).

- **land.slthick.ti-sl-hxy-lnd.fx.glb** (Efx.slthick): Thickness of Soil Layers
Thickness of Soil Layers.

- **landIce.mrfso.tavg-u-hxy-lnd.mon.glb** (Lmon.mrfso): Soil Frozen Water Content
The mass (summed over all all layers) of frozen water.

- **landIce.snc.tavg-u-hxy-lnd.mon.glb** (LImon.snc): Snow Area Percentage
Fraction of each grid cell that is occupied by snow that rests on land portion of cell.

- **landIce.snw.tavg-u-hxy-lnd.mon.glb** (LImon.snw): Surface Snow Amount
Computed as the mass of surface snow on the land portion of the grid cell divided by the land area in the grid cell; reported as missing where the land fraction is 0; excluded is snow on vegetation canopy or on sea ice.

- **ocean.areacello.ti-u-hxy-u.fx.glb** (Ofx.areacello): Grid-Cell Area for Ocean Variables
Cell areas for any grid used to report ocean variables and variables which are requested as used on the model ocean grid (e.g. hfsso, which is a downward heat flux from the atmosphere interpolated onto the ocean grid). These cell areas should be defined to enable exact calculation of global integrals (e.g., of vertical fluxes of energy at the surface and top of the atmosphere).

- **ocean.basin.ti-u-hxy-u.fx.glb** (Ofx.basin): Region Selection Index
A variable with the standard name of region contains strings which indicate geographical regions. These strings must be chosen from the standard region list.

- **ocean.bigthetao.tavg-ol-hxy-sea.mon.glb** (Omon.bigthetao): Sea Water Conservative Temperature
Diagnostic should be contributed only for models using conservative temperature as prognostic field.

- **ocean.deptho.ti-u-hxy-sea.fx.glb** (Ofx.deptho): Sea Floor Depth Below Geoid
Ocean bathymetry. Reported here is the sea floor depth for present day relative to z=0 geoid. Reported as missing for land grid cells.

- **ocean.hfds.tavg-u-hxy-sea.mon.glb** (Omon.hfds): Downward Heat Flux at Sea Water Surface
This is the net flux of heat entering the liquid water column through its upper surface (excluding any "flux adjustment") .

- **ocean.hfgeou.ti-u-hxy-sea.fx.glb** (Ofx.hfgeou): Upward Geothermal Heat Flux at Sea Floor
Upward geothermal heat flux per unit area on the sea floor.

- **ocean.masscello.tavg-ol-hxy-sea.mon.glb** (Omon.masscello): Ocean Grid-Cell Mass per Area
For Boussinesq models, report this diagnostic as Boussinesq reference density times grid celll volume.

- **ocean.mlotst.tavg-u-hxy-sea.mon.glb** (Omon.mlotst): Ocean Mixed Layer Thickness Defined by Delta Sigma T of 0.03 kg m-3 referenced to the model level closest to 10 m depth
Sigma T is potential density referenced to ocean surface. Defined by Sigma T of 0.03 kg m-3 wrt to model level closest to 10 m depth.

- **ocean.sftof.ti-u-hxy-u.fx.glb** (Ofx.sftof): Sea Area Percentage
This is the area fraction at the ocean surface.

- **ocean.so.tavg-ol-hxy-sea.mon.glb** (Omon.so): Sea Water Salinity
Sea water salinity is the salt content of sea water, often on the Practical Salinity Scale of 1978. However, the unqualified term 'salinity' is generic and does not necessarily imply any particular method of calculation. The units of salinity are dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. parts per thousand.

- **ocean.sos.tavg-u-hxy-sea.day.glb** (Oday.sos): Sea Surface Salinity
Sea water salinity is the salt content of sea water, often on the Practical Salinity Scale of 1978. However, the unqualified term 'salinity' is generic and does not necessarily imply any particular method of calculation. The units of salinity are dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. parts per thousand.

- **ocean.sos.tavg-u-hxy-sea.mon.glb** (Omon.sos): Sea Surface Salinity
Sea water salinity is the salt content of sea water, often on the Practical Salinity Scale of 1978. However, the unqualified term 'salinity' is generic and does not necessarily imply any particular method of calculation. The units of salinity are dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. parts per thousand.

- **ocean.tauuo.tavg-u-hxy-sea.mon.glb** (Omon.tauuo): Sea Water Surface Downward X Stress
This is the stress on the liquid ocean from overlying atmosphere, sea ice, ice shelf, etc.

- **ocean.tauvo.tavg-u-hxy-sea.mon.glb** (Omon.tauvo): Sea Water Surface Downward Y Stress
This is the stress on the liquid ocean from overlying atmosphere, sea ice, ice shelf, etc.

- **ocean.thetao.tavg-ol-hxy-sea.mon.glb** (Omon.thetao): Sea Water Potential Temperature
Diagnostic should be contributed even for models using conservative temperature as prognostic field.

- **ocean.thkcello.tavg-ol-hxy-sea.mon.glb** (Omon.thkcello): Ocean Model Cell Thickness
The time varying thickness of ocean cells. "Thickness" means the vertical extent of a layer. "Cell" refers to a model grid-cell.

- **ocean.tos.tavg-u-hxy-sea.day.glb** (Oday.tos): Sea Surface Temperature
This may differ from "surface temperature" in regions of sea ice or floating ice shelves. For models using conservative temperature as the prognostic field, they should report the top ocean layer as surface potential temperature, which is the same as surface in situ temperature.

- **ocean.tos.tavg-u-hxy-sea.mon.glb** (Omon.tos): Sea Surface Temperature
This may differ from "surface temperature" in regions of sea ice or floating ice shelves. For models using conservative temperature as the prognostic field, they should report the top ocean layer as surface potential temperature, which is the same as surface in situ temperature.

- **ocean.umo.tavg-ol-hxy-sea.mon.glb** (Omon.umo): Ocean Mass X Transport
X-ward mass transport from residual mean (resolved plus parameterized) advective transport.

- **ocean.uo.tavg-ol-hxy-sea.mon.glb** (Omon.uo): Sea Water X Velocity
Prognostic x-ward velocity component resolved by the model.

- **ocean.vmo.tavg-ol-hxy-sea.mon.glb** (Omon.vmo): Ocean Mass Y Transport
Y-ward mass transport from residual mean (resolved plus parameterized) advective transport.

- **ocean.vo.tavg-ol-hxy-sea.mon.glb** (Omon.vo): Sea Water Y Velocity
Prognostic y-ward velocity component resolved by the model.

- **ocean.wmo.tavg-ol-hxy-sea.mon.glb** (Omon.wmo): Upward Ocean Mass Transport
Upward mass transport from residual mean (resolved plus parameterized) advective transport.

- **ocean.wo.tavg-ol-hxy-sea.mon.glb** (Omon.wo): Sea Water Vertical Velocity
Prognostic z-ward velocity component resolved by the model.

- **ocean.zos.tavg-u-hxy-sea.day.glb** (Oday.zos): Sea Surface Height Above Geoid
This is the effective dynamic sea level, so should have zero global area mean. zos is the effective sea level as if sea ice (and snow) at a grid cell were converted to liquid seawater (Campin et al., 2008). For OMIP, do _not _record inverse barometer responses from sea-ice (and snow) loading in zos. See (Griffies et al, 2016, https://doi.org/10.5194/gmd-9-3231-2016).

- **ocean.zos.tavg-u-hxy-sea.mon.glb** (Omon.zos): Sea Surface Height Above Geoid
This is the effective dynamic sea level, so should have zero global area mean. It should not include inverse barometer depressions from sea ice.

- **ocean.zostoga.tavg-u-hm-sea.mon.glb** (Omon.zostoga): Global Average Thermosteric Sea Level Change
There is no CMIP6 request for zosga nor zossga.

- **seaIce.siconc.tavg-u-hxy-u.day.glb** (SIday.siconc): Sea-Ice Area Percentage (Ocean Grid)
Percentage of a given grid cell that is covered by sea ice on the ocean grid, independent of the thickness of that ice.

- **seaIce.siconc.tavg-u-hxy-u.mon.glb** (SImon.siconc): Sea-Ice Area Percentage (Ocean Grid)
Percentage of a given grid cell that is covered by sea ice on the ocean grid, independent of the thickness of that ice.

- **seaIce.simass.tavg-u-hxy-si.mon.glb** (SImon.simass): Sea-Ice Mass
Total mass of sea ice divided by grid-cell area.

- **seaIce.sithick.tavg-u-hxy-si.mon.glb** (SImon.sithick): Sea-Ice Thickness
Actual (floe) thickness of sea ice averaged over the ice-covered part of a given grid cell, NOT volume divided by grid area.

- **seaIce.sitimefrac.tavg-u-hxy-sea.mon.glb** (SImon.sitimefrac): Fraction of Time Steps with Sea Ice
Fraction of time steps of the averaging period during which sea ice is present (siconc > 0) in a grid cell.

- **seaIce.siu.tavg-u-hxy-si.mon.glb** (SImon.siu): X-Component of Sea-Ice Velocity
X-component of sea-ice velocity on native model grid.

- **seaIce.siv.tavg-u-hxy-si.mon.glb** (SImon.siv): Y-Component of Sea-Ice Velocity
Y-component of sea-ice velocity on native model grid.

- **seaIce.snd.tavg-u-hxy-sn.mon.glb** (SImon.sisnthick): Snow Thickness
Actual thickness of snow averaged over the snow-covered part of the sea ice. This thickness is usually directly available within the model formulation. It can also be derived by dividing the total volume of snow by the area of the snow.

- **seaIce.ts.tavg-u-hxy-si.mon.glb** (SImon.sitemptop): Surface Temperature of Sea Ice
Mean surface temperature of the sea-ice covered part of the grid cell. Wherever snow covers the ice, the surface temperature of the snow is used for the averaging, otherwise the surface temperature of the ice is used.
