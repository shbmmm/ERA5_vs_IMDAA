#!/usr/bin/env python
# coding: utf-8
import os
import cdsapi

# Ensure the .cdsapirc file exists and is readable
cdsapirc_path = '/home/shubham/w1/internships/prl_2024/.cdsapirc'
if not os.path.exists(cdsapirc_path):
    raise FileNotFoundError(f"The .cdsapirc file was not found at the specified path: {cdsapirc_path}")

# Set the path to your .cdsapirc file if it's not in the home directory
os.environ['CDSAPI_RC'] = cdsapirc_path
c = cdsapi.Client()

def download_data(year):
	c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': '2m_temperature',
        'year': year,
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            22.25, 82.52, 19.25,
            86.51,
        ],
    },
    'download.nc')
# Loop over the years from 2000 to 2023
download_data(2023)





