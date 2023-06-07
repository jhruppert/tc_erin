# Code to plot TS Erin (2007)
# Code adapted from several authors
# Credit given at each step
# Orchestrator: Colin Welty
# June 2023

import xarray as xr
import numpy as np
import netCDF4 as nc
import wrf as wrf
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as crs
from cartopy.feature import (NaturalEarthFeature, STATES)
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ALL_TIMES)
from hraggetvar import wrf_np2da


#filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc"
filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/wrfout_d02_2007-08-19_10:00:00"
# Point to the dataset using 'Dataset'
ds_d01 = xr.open_dataset(filepath)
ncfile = nc.Dataset(filepath)
##For time series:

#Create array of given variable
#da_d01_avo = wrf_np2da(ds_d01,ncfile,'avo')
##For one timestep
#Getvar and print message
avo = getvar(ncfile, "avo")
print("Variable recieved!)")
print(avo)
#Get latitude and logitude points for coordinate
lats, lons = latlon_coords(avo)
#Specify Map Boundaries
lat_min = 32 #these values are currently made up
lat_max = 40
lon_min = -102
lon_max = -94
#Map Details
cmapp = plt.get_cmap('Reds')
#Return projection
proj = wrf.get_cartopy(ncfile)
#Generate plot
fig = plt.figure(figsize=(12,12))
ax = plt.axes(projection=proj)
ax.coastlines('10m', linewidth=0.6)
ax.add_feature(STATES)
plt.contourf(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(avo), 10, cmap = cmapp)
# Add a color bar
cbar = plt.colorbar(ax=ax, shrink=.62)
cbar.set_label(avo.units)
ax.set_xlim(lat_min, lat_max)
ax.set_ylim(lon_min, lon_max)
plt.title("TC Erin Abs. Vorticity")
plt.savefig("erin_avo.png")
plt.close()






