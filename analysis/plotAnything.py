import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import wrf
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Import data
filepath = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/wrfout_d02_2007-'
timeStep = '08-19_10:00:00'

data = Dataset(filepath + timeStep)
pw = wrf.getvar(data, "helicity", wrf.ALL_TIMES)
lats, lons = wrf.latlon_coords(pw)
crs = ccrs.PlateCarree()
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, facecolor='None', projection=crs)
ax.set_extent([-102, -94, 32, 40], crs=crs)
ax.pcolormesh(lons, lats, pw, cmap='coolwarm')
cbar = fig.colorbar(ax.pcolormesh(lons, lats, pw, cmap='inferno'),fraction=0.046, pad=0.04)
cbar.ax.set_ylabel('Helicity (uhh)')

# Add state lines
states = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none',
    edgecolor='white'
)
ax.add_feature(states, linewidth=1.5)
gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
# Customize the title font size and type
title_font = {
    'fontsize': 28,
    'fontweight': 'bold',
    'fontfamily': 'Open Sans'
}
plt.title('Helicity on August 19th at 10:00 UTC', **title_font)

plt.savefig("/home/colinwelty/wrf-stuff/erinproc/helicity-" + timeStep + ".png")
plt.close(fig)
