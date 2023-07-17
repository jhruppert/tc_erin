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
filepath = "/home/colinwelty/wrf-stuff/erinproc/erin3000mtrack_rvor.nc"
filepath3 = "/home/colinwelty/wrf-stuff/erinproc/erinlevel14track_rvor.nc"
filepath2 = "/home/colinwelty/wrf-stuff/erinproc/erin1000mtrack_rvor.nc"
ds = Dataset(filepath)
lats = ds.variables['clat'][:]
lons = ds.variables['clon'][:]

ds2 = Dataset(filepath2)
lats2 = ds2.variables['clat'][:]
lons2 = ds2.variables['clon'][:]

ds3 = Dataset(filepath3)
lats3 = ds3.variables['clat'][:]
lons3 = ds3.variables['clon'][:]

slats = storm.variables['lat'][:]
slons = storm.variables['lon'][:]
#track = ds.variables['track'][:]



fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": ccrs.PlateCarree()})
#storm.plot(ax=ax)  # Plot data on the specified axes
#plt.plot(lons3, lats3, linestyle='--', marker='o', color='g', label='Simulated Track Arbitrary Upper Rvor')

plt.plot(lons, lats, linestyle='--', marker='o', color='b', label='Simulated Track 3000m Rvor')
# plt.plot(lons2, lats2, linestyle='--', marker='o', color='r', label='Simulated Track 1000m Rvor')
plt.plot(slons, slats, linestyle='--', marker='o', color='black', label='Best Track')

ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=1.5, edgecolor='black')
ax.set_extent([-103, -93, 30, 40], crs=ccrs.PlateCarree())
plt.title('Comparison of Simulated and Real Track, Tropical Storm Erin (2007)', fontsize=16)

plt.legend(loc='best')
plt.savefig("bothtrack.png", dpi=300, bbox_inches='tight')
plt.close(fig)




