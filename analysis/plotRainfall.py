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
simData = Dataset(filepath + timeStep)
#Import NOAA Stage IV
stageIVdatapath = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/colin60186/dataxawFxv.tar"
stageIVdata = Dataset(stageIVdatapath)