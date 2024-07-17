import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the data
imdaa = xr.open_dataset('imdaa_TMP_2m_2023_seasmean.nc')
era5 = xr.open_dataset('era5_t2m_2023_regridded_time_v2_seasmean.nc')
difference = xr.open_dataset('diff_seasmean.nc')

# Extract the temperature variables
temp_imdaa = imdaa['TMP_2m']
temp_era5 = era5['t2m']
temp_diff = difference['TMP_2m']

# Determine the extent of the data
lon_min, lon_max = temp_imdaa.longitude.min().item(), temp_imdaa.longitude.max().item()
lat_min, lat_max = temp_imdaa.latitude.min().item(), temp_imdaa.latitude.max().item()

# Create a figure with 4 rows and 3 columns
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18,24), subplot_kw={'projection': ccrs.PlateCarree()})

# List of time labels for labeling
time_labels = [
    'WINTER',
    'SUMMER',
    'MONSOON',
    'POST MONSOON'
]

# Define a function to plot each subplot
def plot_subplot(ax, data, title, cbar_label, cmap, cbar_lim=None, discrete=False):
    if discrete:
        levels = np.arange(cbar_lim[0], cbar_lim[1]+ 0.01, .01)
        norm = plt.Normalize(vmin=cbar_lim[0], vmax=cbar_lim[1])
        im = data.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels, extend='both', cbar_kwargs={'label': cbar_label})
        cbar = im.colorbar
        cbar.set_ticks(levels)
    else:
        im = data.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, cbar_kwargs={'label': cbar_label})
        if cbar_lim:
            im.set_clim(cbar_lim)
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.STATES, linestyle=':')
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.set_title(title, fontsize=15)

for i in range(4):
    # Plot IMD-AA with discretization and specific colorbar limits
    ax1 = axes[i, 0]
    plot_subplot(ax1, temp_imdaa.sel(time=temp_imdaa.time.isel(time=i)), f'IMD-AA {time_labels[i]}', 'relative_humidity [%]', 'rainbow', cbar_lim=(15, 38), discrete=True)

    # Plot ERA5 with discretization and specific colorbar limits
    ax2 = axes[i, 1]
    plot_subplot(ax2, temp_era5.sel(time=temp_era5.time.isel(time=i)), f'ERA5 {time_labels[i]}', 'relative_humidity [%]', 'rainbow', cbar_lim=(15, 38), discrete=True)

    # Plot Difference without specific colorbar limits
    ax3 = axes[i, 2]
    plot_subplot(ax3, temp_diff.sel(time=temp_diff.time.isel(time=i)), f'Difference {time_labels[i]}', 'difference in relative_humidity [%]', 'coolwarm')

# Add main title and adjust layout
plt.suptitle('Seasonal wind_speed Comparison (IMD-AA vs ERA5)', fontsize=16, y=0.95)
plt.tight_layout()
plt.subplots_adjust(top=0.92)  # Adjust top to fit the suptitle

# Save the figure
plt.savefig('seasonal_relative_humidity difference_comparison.png', dpi=150)

# Show the plot
#plt.show()

