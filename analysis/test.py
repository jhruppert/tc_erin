from netCDF4 import Dataset

# Open the NetCDF file
file_path = '/ourdisk/hpc/radclouds/auto_archive_notyet/tape_2copies/tc_erin/stitchd02_wrfout.nc'
nc_file = Dataset(file_path, 'r')

# Read the variable data
v_data = nc_file.variables['V'][:, 2, :]

# Print the values along the second axis
for value in v_data:
    print(value)

# Print the number of values
print("Number of values:", len(v_data))

# Close the NetCDF file
nc_file.close()