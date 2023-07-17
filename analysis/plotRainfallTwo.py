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
grib_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081918.06h"
nc_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081918.06h.nc"


# Open the GRIB file
grib_data = xr.open_dataset(grib_filepath, engine="cfgrib")
grib_data.to_netcdf(nc_filepath)
grib_data.close()

# Import data
directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/'  # Replace with the path to your directory
prefix = 'wrfout_d02'
timeStep = '08-19_18:00:00'
timeStepSub = '08-19_12:00:00'
simData = Dataset(directory+prefix+"_2007-" + timeStep)
subSimData = Dataset(directory+prefix+"_2007-" + timeStepSub)
#Import NOAA Stage IV
stageIVdatapath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081918.06h.nc"
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

# Coarsen the simulated WRF rainfall data
coarsening_factor = 1 # Adjust this factor to change the coarseness
coarse_lon = lon[::coarsening_factor, ::coarsening_factor]
coarse_lat = lat[::coarsening_factor, ::coarsening_factor]
coarse_precip = precip[::coarsening_factor, ::coarsening_factor]

#Get StageIV variables
rlon = stageIVdata.variables['longitude']
rlat = stageIVdata.variables['latitude']
tp = stageIVdata.variables['tp']

#Establish projection

crs = ccrs.PlateCarree()

# Create the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'projection': crs})
plt.subplots_adjust(wspace=0.3)

# Set the extent for both subplots LEGACY
#ax1.set_extent([-102, -96, 32, 38], crs=crs)
#ax2.set_extent([-102, -96, 32, 38], crs=crs)

# Set the extent for both subplots 
ax1.set_extent([-99.5, -93.5, 33, 39], crs=crs)
ax2.set_extent([-99.5, -93.5, 33, 39], crs=crs)

nws_precip_colors = [
    "#fdfdfd",
    "#a9f5f4",  # 0.01 - 0.10 inches
    "#33aff2",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches 
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
    "#fdfdfd"   # 10.00+
]
precip_colormap = mpl.colors.ListedColormap(nws_precip_colors)
levels = [0.0, 0.25, 2.5, 6, 12.5, 19, 25, 38, 51, 64, 76, 102, 127,
          152, 203, 254, 508]
norm = mpl.colors.BoundaryNorm(levels, 16)

ax1.pcolormesh(coarse_lon, coarse_lat, coarse_precip, norm=norm, cmap=precip_colormap)
cbar1 = fig.colorbar(ax1.collections[0], ax=ax1, orientation='horizontal', fraction=0.046, pad=0.04, extend='max', ticks=levels)
cbar1.ax.set_xlabel('Rainfall in mm')
cbar1.ax.tick_params(labelsize=7)

ax2.pcolormesh(rlon, rlat, tp, norm=norm, cmap=precip_colormap)
cbar2 = fig.colorbar(ax2.collections[0], ax=ax2, orientation='horizontal', fraction=0.046, pad=0.04, extend='max', ticks=levels)
cbar2.ax.set_xlabel('Rainfall in mm')
cbar2.ax.tick_params(labelsize=7)

# Add state lines
states = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none',
    edgecolor='black',
    #linewidth=1.0  # Reduced linewidth for state lines
)
ax1.add_feature(states)
ax2.add_feature(states)

ax1.set_title("Simulated WRF Rainfall", fontsize=18)
ax2.set_title("NOAA Stage IV Rainfall", fontsize=18)

#ax1.gridlines(draw_labels=False)  # Remove gridlines
#ax2.gridlines(draw_labels=False)  # Remove gridlines

# Customize the title font size and type
title_font = {
    'fontsize': 20,
    'fontweight': 'bold',
    'fontfamily': 'Open Sans'
}
fig.suptitle('6 Hour Rainfall Comparison at 18:00 UTC on August 19th, 2007', **title_font)

plt.tight_layout()  # Apply tight layout

plt.savefig("/home/colinwelty/wrf-stuff/erinproc/rainfallsimtest-" + timeStep + "-6.png")
plt.close(fig)