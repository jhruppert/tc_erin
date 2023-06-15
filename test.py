from netCDF4 import Dataset

# Open the NetCDF file
file_path = 'stitchd02_wrfout.nc'
nc_file = Dataset(file_path, 'r')

# Read the variable data
v_data = nc_file.variables['V'][:, :, 1]

# Print the values along the second axis
for value in v_data:
    print(value)

# Close the NetCDF file
nc_file.close()