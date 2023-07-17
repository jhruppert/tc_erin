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
import matplotlib as mpl


# # Specify the input and output file paths
# grib_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h"
# nc_filepath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h.nc"


# # Open the GRIB file
# grib_data = xr.open_dataset(grib_filepath, engine="cfgrib")
# grib_data.to_netcdf(nc_filepath)
# grib_data.close()

# Import data
directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/'  # Replace with the path to your directory
prefix = 'wrfout_d02'
timeStep = '08-20_00:00:00'
timeStepSub = '08-19_23:00:00'
simData = Dataset(directory+prefix+"_2007-" + timeStep)
subSimData = Dataset(directory+prefix+"_2007-" + timeStepSub)
#Import NOAA Stage IV
# stageIVdatapath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/ST4.2007081910.01h.nc"
# stageIVdata = Dataset(stageIVdatapath)
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

# print("Shape of precip:", precip.shape)
# print("Shape of lon:", lon.shape)
# print("Shape of lat:", lat.shape)
# print("Variables: ", stageIVdata.variables)
# rlon = stageIVdata.variables['longitude']
# rlat = stageIVdata.variables['latitude']
# tp = stageIVdata.variables['tp']


#Add projection
crs = ccrs.PlateCarree()

# Create the figure and subplots
fig, (ax1) = plt.subplots(figsize=(12, 6), subplot_kw={'projection': crs})

# Set the extent for both subplots
ax1.set_extent([-104, -95, 30, 39], crs=crs)

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

# Plot simulated WRF rainfall
pcm1 = ax1.pcolormesh(lon, lat, precip, norm = norm, cmap=precip_colormap, transform=crs)

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

# Set titles and labels
ax1.set_title("Simulated WRF Rainfall", fontsize=12)

# Remove gridlines
ax1.gridlines(draw_labels=False)

# Adjust spacing and layout
plt.tight_layout()

# Save the figure
plt.savefig("/home/colinwelty/wrf-stuff/erinproc/rain/rainfallsimtest-" + timeStep + ".png", dpi=300)
plt.close(fig)