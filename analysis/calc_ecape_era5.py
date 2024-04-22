# ------------------------------------------------
# Name: calc_ecape_era5.py
# Author: Robby M. Frost
# University of Oklahoma
# Created: 09 April 2024
# Purpose: Script for calculating ECAPE over a 
# 2D horizontal field of ERA5 data
# ------------------------------------------------
# imports
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from ecape_parcel.calc import calc_ecape_parcel
from ecape_parcel.ecape_calc import calc_ecape
import metpy.calc as mpcalc
from metpy.calc import dewpoint_from_specific_humidity, parcel_profile, cape_cin
from metpy.units import units
from metpy.plots import SkewT
import matplotlib.pyplot as plt
import sounderpy as spy
from datetime import datetime
import requests
# ------------------------------------------------
# settings

# directory for data to be output
dout = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/robby/erin/ecape/"

# date information
year  = '2007' 
month = '08'
day   = '17'

# latitude and longitude ranges
min_lat = 25
max_lat = 38
lat = np.arange(min_lat, max_lat+0.1, 1)
min_lon = -105
max_lon = -92
lon = np.arange(min_lon, max_lon-0.1, 1)

model = 'rap'

# ------------------------------------------------
# ECAPE calculation

# arrays to hold ecape values and datetime array
ecape = np.empty((8,lat.size,lon.size))
time = []

# list of hours
hrs = [0,3,6,9,12,15,18,21]

# loop over time
for jh in range(len(hrs)):
    # set hour
    if jh < 4:
        hour = f"0{hrs[jh]}"
    else:
        hour = str(hrs[jh])

    # set up time index
    date_string = f"{year}-{month}-{day} {hour}:00:00"
    # Convert the string to a numpy datetime object
    numpy_datetime = np.datetime64(datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S'))
    # store in list
    time.append(numpy_datetime)

    # loop over lat/lon
    for jlat in range(lat.size):
        for jlon in range(lon.size):

            # set latlon list
            latlon = [lat[jlat],lon[jlon]]
            # pull vertical profile from ERA5
            try:
                clean_data = spy.get_model_data(model, latlon, year, month, day, hour)
            except ValueError:
                print(f"Value Error, skipping lat/lon = {latlon}, jh = {jh}")
                continue
            except requests.exceptions.HTTPError:
                print(f"HTTP Error, skipping lat/lon = {latlon}, jh = {jh}")
                continue

            # extract variables
            p = clean_data['p']
            T = clean_data['T']
            Td = clean_data['Td']
            z = clean_data['z']
            u = clean_data['u']
            v = clean_data['v']

            # calculate specific humidity
            q = mpcalc.specific_humidity_from_dewpoint(p,Td)
            # calculate ecape and story in array
            try:
                ecape[jh,jlat,jlon] = calc_ecape(z, p, T, q, u, v, cape_type="mixed_layer", storm_motion="mean_wind").magnitude
            except AttributeError:
                print(f"Attribute Rrror, skipping lat/lon = {latlon}, jh = {jh}")
                continue
            except requests.exceptions.HTTPError:
                print(f"HTTP Error, skipping lat/lon = {latlon}, jh = {jh}")
                continue
            except TimeoutError:
                print(f"Timeout Error, skipping lat/lon = {latlon}, jh = {jh}")
                continue
# ------------------------------------------------
# Create a Dataset to hold the ECAPE data
ecape_ds = xr.Dataset()

# Add dimensions and coordinates to the Dataset
ecape_ds['time'] = time
ecape_ds['latitude'] = lat
ecape_ds['longitude'] = lon

# Add the ECAPE variable to the Dataset
ecape_ds['ecape'] = (('time', 'latitude', 'longitude'), ecape)

# Add attributes
ecape_ds.attrs['description'] = "ECAPE calculated over the domain using ERA5 data"
ecape_ds.attrs['units'] = "J/kg"

# Save the Dataset to a NetCDF file
fsave = f"{dout}ecape_{year}{month}{day}.nc"
ecape_ds.to_netcdf(fsave)

print(f"Successfully output to {fsave}, script complete!")
# ------------------------------------------------
# # read in data
# pl = xr.open_dataset("/home/robbyfrost/era5/ERA5-20070817-20070821-pl.nc")

# # narrow down time dimension
# pl = pl.isel(time=slice(0,24))
# # latitude and longitude ranges
# min_lat = 25
# max_lat = 38
# min_lon = -105
# max_lon = -92
# # Create boolean masks for latitude and longitude
# lat_mask = (pl['latitude'] >= min_lat) & (pl['latitude'] <= max_lat)
# lon_mask = (pl['longitude'] >= min_lon) & (pl['longitude'] <= max_lon)
# # Apply the masks to your dataset
# subset_ds = pl.where(lat_mask & lon_mask, drop=True)
# # Flip the order of the 'level' dimension
# pl = pl.reindex(level=pl.level[::-1])
# pl = pl.isel(level=slice(4,36))

# # extract dimensions
# height = (pl.z.values / 9.81) * units("m")
# height = height
# pressure = pl.level.values * units("hPa")
# lat1d, lon1d = pl.latitude, pl.longitude
# nlat, nlon = lat1d.size, lon1d.size
# time = pl.time
# ntime = time.size
# # Need 2d lat, lon grid
# lat, lon = np.meshgrid(lat1d, lon1d, indexing='ij')

# # extract variables
# T = pl.t.values * units("K")
# T = T.to("degC")
# q = pl.q.values * units("kg/kg")
# u = pl.u.values * units("m/s")
# v = pl.v.values * units("m/s")


# # ------------------------------------------------
# # calculate ecape at one point (TESTING)
# ecape = np.empty(ntime)
# for jt in range(ntime):
#     ecape = calc_ecape(height_msl=height[jt,:,68,125], pressure=pressure, 
#                     temperature=T[jt,:,68,125], specific_humidity=q[jt,:,68,125], 
#                     u_wind=u[jt,:,68,125], v_wind=v[jt,:,68,125],
#                     cape_type="mixed_layer")
#     print(ecape)

# ------------------------------------------------
# # calculate ECAPE over whole domain
# ecape = np.empty((ntime,nlat,nlon))

# # for jt in range(ntime):
# jt = 0
#     # print("jt = ", jt, "\n")
# for jlon in range(nlon):
#     for jlat in range(nlat):
#         # try:
#         ecape[jt, jlon, jlat] = calc_ecape(height_msl=height[jt,:,jlon,jlat],
#                                             pressure=pressure,
#                                             temperature=T[jt,:,jlon,jlat],
#                                             specific_humidity=q[jt,:,jlon,jlat],
#                                             u_wind=u[jt,:,jlon,jlat],
#                                             v_wind=v[jt,:,jlon,jlat],
#                                             cape_type="mixed_layer")
#         # except IndexError:
#         #     ecape[jt, jlat, jlon] = 0
#         #     continue
#         # except ValueError:
#         #     continue