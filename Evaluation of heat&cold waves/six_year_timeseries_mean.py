import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Load the NetCDF files
file1 = 'era5_daymax_C.nc'
file2 = 'imdaa_daymax_C.nc'

ds1 = xr.open_dataset(file1)
ds2 = xr.open_dataset(file2)

# Assuming the variable of interest is named 'temperature' in both files
var1 = ds1['t2m']
var2 = ds2['TMP_2m']

# Apply rolling mean (e.g., 30-day window)
rolling_window = 30
var1_smoothed = var1.rolling(time=rolling_window, center=True).mean()
var2_smoothed = var2.rolling(time=rolling_window, center=True).mean()

# Time coordinates
time1 = ds1['time']
time2 = ds2['time']

# Plotting
plt.figure(figsize=(14, 7))

# Plot the smoothed data
plt.plot(time1, var1_smoothed.mean(dim=['latitude', 'longitude']), label='ERA5', color='blue', linestyle='-', linewidth=2)
plt.plot(time2, var2_smoothed.mean(dim=['latitude', 'longitude']), label='IMD-AA', color='orange', linestyle='-', linewidth=2)

# Enhancing the plot
plt.title('Time Series of Temperature for Odisha (2018-2023) - 30 Day Moving Average', fontsize=16)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Temperature (°C)', fontsize=14)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

# Improve the x-axis date formatting and locator
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Increase the number of ticks on the y-axis
plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=20))

plt.tight_layout()
plt.savefig("timeseries_mean_improved.png", dpi=300)
plt.show()

# Close the datasets
ds1.close()
ds2.close()

