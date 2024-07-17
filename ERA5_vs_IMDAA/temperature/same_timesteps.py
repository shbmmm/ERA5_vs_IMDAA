import netCDF4 as nc
import numpy as np

# Function to get indices of common times
def get_common_time_indices(time1_dates, time2_dates):
    common_times = np.intersect1d(time1_dates, time2_dates)
    indices1 = np.nonzero(np.in1d(time1_dates, common_times))[0]
    return indices1

# Load both NetCDF files
file1 = 'era5_t2m_2023_regridded.nc'
file2 = 'imdaa_TMP_2m_2023.nc'

ds1 = nc.Dataset(file1, 'r')
ds2 = nc.Dataset(file2, 'r')

# Extract time variables from both datasets
time1 = ds1.variables['time'][:]
time2 = ds2.variables['time'][:]

# Convert times to datetime objects for comparison
time1_dates = nc.num2date(time1, ds1.variables['time'].units)
time2_dates = nc.num2date(time2, ds2.variables['time'].units)

# Get the indices of the common times in the original time array
indices1 = get_common_time_indices(time1_dates, time2_dates)

# Create a new NetCDF file for the aligned data
with nc.Dataset('era5_t2m_2023_regridded_time.nc', 'w', format='NETCDF4') as ds1_aligned:
    # Copy dimensions from the original dataset
    for name, dimension in ds1.dimensions.items():
        if name == 'time':
            ds1_aligned.createDimension(name, len(indices1))
        else:
            ds1_aligned.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
    
    # Copy variables, trimming time and associated data
    for name, variable in ds1.variables.items():
        var_dims = variable.dimensions
        if 'time' in var_dims:
            # Assuming time is the first dimension for variables with 'time'
            var = ds1_aligned.createVariable(name, variable.datatype, var_dims, zlib=True, complevel=4)
            var.setncatts({k: variable.getncattr(k) for k in variable.ncattrs()})
            # Read and write data in chunks to save memory
            chunk_size = 1000  # Adjust chunk size based on available memory
            for start in range(0, len(indices1), chunk_size):
                end = min(start + chunk_size, len(indices1))
                var[start:end] = variable[indices1[start:end]]
        else:
            # Variables without 'time' dimension
            var = ds1_aligned.createVariable(name, variable.datatype, var_dims, zlib=True, complevel=4)
            var.setncatts({k: variable.getncattr(k) for k in variable.ncattrs()})
            var[:] = variable[:]

# Close the original datasets
ds1.close()
ds2.close()

