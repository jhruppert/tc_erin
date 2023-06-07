import xarray as xr
import numpy as np
import netCDF4 as nc
import wrf as wrf
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ALL_TIMES)
from hraggetvar import wrf_np2da


filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc"

# Point to the dataset using 'Dataset'
ds_d01 = xr.open_dataset(filepath)
ncfile = nc.Dataset(filepath)
#Create array of given variable
da_d01_P = wrf_np2da(ds_d01,ncfile,'pressure')
#Get latitude and logitude points for coordinate
lats, lons = wrf.latlon_coords(da_d01_P)
#Specify Map Boundaries
lat_min = 1 #these values are currently made up
lat_max = 2
lon_min = 1
lon_max = 2
#Map Details
cmap = plt.get_cmap('Reds')
crss = crs.PlateCarree()
#Create plot- adapted from BA on medium.com
fig = plt.figure(figsize=(10,6))    
ax = fig.add_subplot(111, facecolor='None', projection=crss)
ax.coastlines(resolution='10m', alpha=0.5)
plotp= ax.pcolormesh(lons, lats, da_d01_P, cmap=cmap)
cbar = fig.colorbar(plotp)
cbar.ax.set_ylabel('Pressure in Pa')
# set other plot parameters
plt.xlim((lon_min,lon_max))
plt.ylim((lat_min, lat_max))
plt.title('TC Erin Pressure')
plt.show()






