from distutils.log import info
from netCDF4 import Dataset
import numpy as np
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
var_tag = 'pressure'
basis = 0

# ------------------------------------------
# File pattern
filepattern = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/colin/erin/test/output/raw/wrfout_d02*'
filepaths = glob.glob(filepattern)
Data = []
for filepath in filepaths:
    dataset = Dataset(filepath)
    Data.append(dataset)

varname = 'pressure'
var = wrf.getvar(Data, varname)
lon = []
lat = []

max_iterations = 200  # Maximum number of iterations to prevent infinite loop
iteration_count = 0

for dataset in Data:
    lon.append(dataset.variables['XLONG'][:])  # deg
    lat.append(dataset.variables['XLAT'][:])  # deg

    iteration_count += 1
    if iteration_count > max_iterations:
        raise Exception("Exceeded maximum iteration count. Possible infinite loop detected.")

lon = np.array(lon)
lat = np.array(lat)
lon1d = lon[0, :]
lat1d = lat[:, 0]
#lat, lon = wrf.latlon_coords(var)


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