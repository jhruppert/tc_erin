from distutils.log import info
from netCDF4 import Dataset
import numpy as np
import os
import sys
import subprocess
import xarray as xr
from track_tc import object_track
#from hraggetvar import wrf_np2da
import wrf
import glob


# Choices
#ptrack  = 600 # tracking pressure level
#istorm  = 'haiyan'
# istorm  = 'maria'
# imemb   = 'memb_01'
# itest   = 'ctl'
#itest   = 'ncrf36h'
# itest   = 'ncrf48h'
# itest   = 'crfon60h'
istorm = 'erin'
i_senstest = 'none'
var_tag = 'avo'
basis = 0

# ------------------------------------------
# File pattern
directory = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw'  # Replace with the path to your directory
prefix = 'wrfout_d02'  # Replace with the desired file prefix

#file_count = sum(1 for file in os.listdir(directory) if file.startswith(prefix))
 # Replace with the desired number of files to process

# Get a list of files in the directory that start with the given prefix
#file_list = [file for file in os.listdir(directory) if file.startswith(prefix)]

# Sort the file list to ensure consistent processing order
#file_list.sort()
varname = 'avo'
# Iterate over the specified number of files or the available files if fewer
#lat_accum = None
#lon_accum = None
#var_accum = None

#for i, file_to_load in enumerate(file_list[:file_count]):
#    file_path = os.path.join(directory, file_to_load)
#    print(f"Processing file {i+1}: {file_path}")
#    Data = wrf.getvar(Dataset(file_path), varname, timeidx=wrf.ALL_TIMES)
#    
#    if lat_accum is None:
#        lat_accum = wrf.latlon_coords(Data)[0]
#        lon_accum = wrf.latlon_coords(Data)[1]
#        var_accum = Data.values
#    else:
#        lat_accum += wrf.latlon_coords(Data)[0]
#        lon_accum += wrf.latlon_coords(Data)[1]
#        var_accum += Data.values
#
#lat = xr.DataArray(lat_accum)
#lon = xr.DataArray(lon_accum)
#f = xr.DataArray(var_accum, dims=('time', 'y', 'x'))

process = subprocess.Popen(['ls '+directory+'/'+ prefix+'*'],shell=True,
    stdout=subprocess.PIPE,universal_newlines=True)
output = process.stdout.readline()
m1ctl = output.strip() #[3]
fil = Dataset(m1ctl) # this opens the netcdf file
lon = fil.variables['XLONG'][:][0] # deg
lon1d=lon[0,:]
lat = fil.variables['XLAT'][:][0] # deg
lat1d=lat[:,0]
Data = Dataset('/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc')
var = wrf.getvar(Dataset('/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc'), varname, timeidx=wrf.ALL_TIMES)
print (var.shape)
print (lon.shape)
if var.shape!= (3):
    print("The shape is all wrong bro")

fil.close()
llshape=np.shape(lon)
nx = llshape[1]
ny = llshape[0]


# Run tracking
track, var_masked = object_track(var, lon, lat, i_senstest, basis)
    
clon = track[0, :]
clat = track[1, :]

# Write out to netCDF file
file_out = istorm + 'track_' + var_tag + '.nc'
ncfile = Dataset(file_out, mode='w')

time_dim = ncfile.createDimension('time', len(wrf.extract_times(Data, wrf.ALL_TIMES)))

clat = ncfile.createVariable('clat', np.float64, ('time',))
clat.units = 'degrees_north'
clat.long_name = 'clat'
clat[:] = track[1, :]

clon = ncfile.createVariable('clon', np.float64, ('time',))
clon.units = 'degrees_east'
clon.long_name = 'clon'
clon[:] = track[0, :]

ncfile.close()

print("Done!") 