import os
import xarray as xr
import wrf 
from netCDF4 import Dataset


directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw'  # Replace with the path to your directory
prefix = 'wrfout_d02'  # Replace with the desired file prefix

file_count = sum(1 for file in os.listdir(directory) if file.startswith(prefix))
 # Replace with the desired number of files to process

# Get a list of files in the directory that start with the given prefix
file_list = [file for file in os.listdir(directory) if file.startswith(prefix)]

# Sort the file list to ensure consistent processing order
file_list.sort()
f = xr.DataArray()
lat = xr.DataArray()
lon = xr.DataArray()
varname = 'pres'
# Iterate over the specified number of files or the available files if fewer
for i, file_to_load in enumerate(file_list[:file_count]):
    file_path = os.path.join(directory, file_to_load)
    print(f"Processing file {i+1}: {file_path}")
    Data = Dataset(file_path)
    var = wrf.getvar(Data, varname, timeidx=wrf.ALL_TIMES)
    lats, lons = wrf.latlon_coords(var)
    lat += lats
    lon += lons
    f += var

    
print("done")