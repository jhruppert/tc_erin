# quick script to mask interpolated AGL tc winds from WRF output
import sys
sys.path.append("/home/robbyfrost/jhr-wrf-python/")
from mask_tc_track import mask_tc_track
import xarray as xr
import numpy as np

# paths to files
dstitch = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc"
duc = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/c_aglinterp_U"
dvc = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/c_aglinterp_V"
dud = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/d_aglinterp_U"
dvd = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/d_aglinterp_V"
dctrack = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/erin3000track_rvor.nc"
ddtrack = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/analysis/erin_d3000track_rvor.nc"

# read in stitched output
ds = xr.open_dataset(dstitch)
# read in plev interpolated values
u_c = xr.open_dataset(duc).U
v_c = xr.open_dataset(dvc).V
u_d = xr.open_dataset(dud).U
v_d = xr.open_dataset(dvd).V
# assign pressure levels to height coordinate
u_c["bottom_top"] = np.arange(0,5000.1,200)
u_d["bottom_top"] = np.arange(0,5000.1,200)
v_c["bottom_top"] = np.arange(0,5000.1,200)
u_d["bottom_top"] = np.arange(0,5000.1,200)
# extract dimensions
lat = ds.XLAT[0].values
lon = ds.XLONG[0].values
time = ds.XTIME

# mask dataset to follow tc track
print("Masking wind arrays \n")
uc_mask = mask_tc_track(track_file=dctrack, rmax=1, var=u_c, 
                        lon_tmp=lon, lat=lat, t0=0, t1=61)
ud_mask = mask_tc_track(track_file=ddtrack, rmax=1, var=u_d, 
                        lon_tmp=lon, lat=lat, t0=0, t1=61)
vc_mask = mask_tc_track(track_file=dctrack, rmax=1, var=v_c, 
                        lon_tmp=lon, lat=lat, t0=0, t1=61)
vd_mask = mask_tc_track(track_file=ddtrack, rmax=1, var=v_d, 
                        lon_tmp=lon, lat=lat, t0=0, t1=61)

print("Calculating WSPD \n")
wspd_c = (uc_mask ** 2 + vc_mask ** 2) ** (1/2)
wspd_d = (ud_mask ** 2 + vd_mask ** 2) ** (1/2)

# create dataset with all 4 arrays
print("Creating dataset \n")
masked_wind_ds = xr.Dataset(
    data_vars=dict(
        u_control=(["time", "z", "lon", "lat"], uc_mask),
        v_control=(["time", "z", "lon", "lat"], vc_mask),
        wspd_control=(["time", "z", "lon", "lat"], wspd_c),
        u_diurnal=(["time", "z", "lon", "lat"], ud_mask),
        v_diurnal=(["time", "z", "lon", "lat"], vd_mask),
        wspd_diurnal=(["time", "z", "lon", "lat"], wspd_d)
    ),
    coords=dict(
        time=time.values,
        z=u_c.bottom_top.values,
        longitude=(["lon", "lat"], lon),
        latitude=(["lon", "lat"], lat)
    ),
    attrs=dict(description="Masked WRF TC winds based on the 3000 meter relative vorticity track"),
)

# output to netcdf
fsave = "/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/robby/erin/mask_tc_wind/masked_tc_winds_agl_3000mtrack_1deg.nc"
print(f"Saving dataset to {fsave} \n")
masked_wind_ds.to_netcdf(fsave)
print("Finished!")