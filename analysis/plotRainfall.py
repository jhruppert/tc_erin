import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import wrf
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import subprocess
import cfgrib
import xarray as xr


# Specify the input and output file paths
grib_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h"
nc_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h.nc"


# Open the GRIB file
grib_data = xr.open_dataset(grib_filepath, engine="cfgrib")
grib_data.to_netcdf(nc_filepath)
grib_data.close()

# Import data
directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/'  # Replace with the path to your directory
prefix = 'wrfout_d02'
timeStep = '08-19_10:00:00'
timeStepSub = '08-19_09:00:00'
simData = Dataset(directory+prefix+"_2007-" + timeStep)
subSimData = Dataset(directory+prefix+"_2007-" + timeStepSub)
#Import NOAA Stage IV
stageIVdatapath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h.nc"
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


#Add projection
crs = ccrs.PlateCarree()

# Create the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'projection': crs})

# Set the extent for both subplots
ax1.set_extent([-102, -96, 32, 38], crs=crs)
ax2.set_extent([-102, -96, 32, 38], crs=crs)

# Plot simulated WRF rainfall
pcm1 = ax1.pcolormesh(lon, lat, precip, cmap='PuBu', transform=crs)

# Add state lines with higher zorder to ensure visibility
states = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none',
    edgecolor='black'
)
ax1.add_feature(states, linewidth=0.5, zorder=3)

cbar1 = fig.colorbar(pcm1, ax=ax1, orientation='horizontal', pad=0.05)
cbar1.ax.set_xlabel('Rainfall in mm')

# Plot NOAA Stage IV rainfall
pcm2 = ax2.pcolormesh(rlon, rlat, tp, cmap='PuBu', transform=crs)

# Add state lines with higher zorder to ensure visibility
ax2.add_feature(states, linewidth=0.5, zorder=3)

cbar2 = fig.colorbar(pcm2, ax=ax2, orientation='horizontal', pad=0.05)
cbar2.ax.set_xlabel('Rainfall in mm')

# Set titles and labels
ax1.set_title("Simulated WRF Rainfall", fontsize=12)
ax2.set_title("NOAA Stage IV Rainfall", fontsize=12)

# Remove gridlines
ax1.gridlines(draw_labels=False)
ax2.gridlines(draw_labels=False)

# Adjust spacing and layout
plt.tight_layout()

# Save the figure
plt.savefig("/home/colinwelty/wrf-stuff/erinproc/rainfallsim-" + timeStep + ".png", dpi=300)
plt.close(fig)