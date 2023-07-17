import netCDF4
from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import wrf
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import subprocess
import cfgrib
import xarray as xr


# Specify the input and output file paths
grib_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081912.24h"
nc_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081912.24h.nc"


# Open the GRIB file
grib_data = xr.open_dataset(grib_filepath, engine="cfgrib")
grib_data.to_netcdf(nc_filepath)
grib_data.close()

# Import data
directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/'  # Replace with the path to your directory
prefix = 'wrfout_d02'
timeStep = '08-19_12:00:00'
timeStepSub = '08-18_12:00:00'
simData = Dataset(directory+prefix+"_2007-" + timeStep)
subSimData = Dataset(directory+prefix+"_2007-" + timeStepSub)
#Import NOAA Stage IV
stageIVdatapath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081912.24h.nc"
stageIVdata = Dataset(stageIVdatapath)
process = subprocess.Popen(['ls '+directory+prefix+"_2007-" + timeStep],shell=True,
    stdout=subprocess.PIPE,universal_newlines=True)
output = process.stdout.readline()
m1ctl = output.strip() #[3]
fil = Dataset(m1ctl) # this opens the netcdf file
lon = fil.variables['XLONG'][:][0] # deg
lon1d=lon[0,:]
print("Longitude? Recieved!")
lat = fil.variables['XLAT'][:][0] # deg
lat1d=lat[:,0]
rainfallConvec = fil.variables['RAINC']
rainfallNC = fil.variables['RAINNC']
precip = rainfallConvec[:]+rainfallNC[:]
precip1 = precip[0,:,:]
#Repeat Process for Previous TimeStep
process = subprocess.Popen(['ls '+directory+prefix+"_2007-" + timeStepSub],shell=True,
    stdout=subprocess.PIPE,universal_newlines=True)
output = process.stdout.readline()
m1ctl = output.strip() #[3]
fil = Dataset(m1ctl)
rainfallConvec = fil.variables['RAINC']
rainfallNC = fil.variables['RAINNC']
precip = rainfallConvec[:]+rainfallNC[:]
precip2 = precip[0,:,:]

#Subtract for Rainfall Rate
precip = precip1 - precip2

print("Shape of precip:", precip.shape)
print("Shape of lon:", lon.shape)
print("Shape of lat:", lat.shape)
print("Variables: ", stageIVdata.variables)
rlon = stageIVdata.variables['longitude']
rlat = stageIVdata.variables['latitude']
tp = stageIVdata.variables['tp']

anom = tp - precip

crs = ccrs.PlateCarree()
# Create the figure and subplots
# Create the figure and subplots
fig, ax = plt.subplots(figsize=(14, 10), subplot_kw={'projection': crs})

# Set the extent for both subplots
ax.set_extent([-102, -96, 32, 38], crs=crs)


ax.pcolormesh(lon, lat, anom, cmap="coolwarm")
cbar1 = fig.colorbar(ax.collections[0], ax=ax, fraction=0.046, pad=0.04, extend='max')
cbar1.ax.set_ylabel('Rainfall Anomaly in Millimeters')



# Add state lines
states = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none',
    edgecolor='black'
)
ax.add_feature(states, linewidth=1.5)

gl1 = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)


# Customize the title font size and type
title_font = {
    'fontsize': 28,
    'fontweight': 'bold',
    'fontfamily': 'Open Sans'
}
fig.suptitle('24 Hour Rainfall Anomaly Between Simulated and Observed', **title_font)

plt.savefig("/home/colinwelty/wrf-stuff/erinproc/rainfallanom-" + timeStep + "24.png")
plt.close(fig)