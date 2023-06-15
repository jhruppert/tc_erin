import netCDF4
from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import wrf
import pandas as pd
import tropycal.tracks as tracks
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#Import Dataset for Best Track Data
url = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-042723.txt"
basin = tracks.TrackDataset(basin='north_atlantic', atlantic_url=url)
storm = basin.get_storm(('erin',2007))
storm = storm.to_xarray()
#Import netCDF file for Simulated Track
filepath = "/home/colinwelty/wrf-stuff/erinproc/erintrack_avo.nc"
ds = Dataset(filepath)
lats = ds.variables['clat'][:]
lons = ds.variables['clon'][:]

slats = storm.variables['lat'][:]
slons = storm.variables['lon'][:]
#track = ds.variables['track'][:]



fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": ccrs.PlateCarree()})
#storm.plot(ax=ax)  # Plot data on the specified axes
plt.plot(lons, lats, linestyle='--', marker='o', color='b', label='Simulated Track')
plt.plot(slons, slats, linestyle='--', marker='o', color='black', label='Best Track')
ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=1.5, edgecolor='black')
ax.set_extent([-103, -93, 30, 40], crs=ccrs.PlateCarree())
plt.legend(loc='best')

fig.savefig("bothtrack.png")
plt.close(fig)  # Close the figure object




