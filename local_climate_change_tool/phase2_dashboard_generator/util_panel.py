"""
util_panel.py

Module of functions for creating data that the climate_dashboard panel reads in.
"""

import sys
import pandas as pd
import xarray as xr


DIR_ANALYSIS = '../phase1_data_wrangler'
sys.path.insert(0, DIR_ANALYSIS)
import analysis_parameters


DF = pd.read_csv('worldcities.csv')
COUNTRIES = list(set(DF['country']))
THIS_EXPERIMENT_ID = ['historical', 'ssp126', 'ssp370', 'ssp245', 'ssp585']
EXPERIMENT_KEYS = THIS_EXPERIMENT_ID.copy()
EXPERIMENT_KEYS.append('historical_obs')


def read_data():
    """Reads in the data.

    Reads in the data and returns a dictionary for data_type with keys
    'historical', 'ssp126', 'ssp370', 'ssp245', 'ssp585', and 'historical_obs'.

    Returns:
        dict_timeseries: The data_type dictionary.
    """
    dict_timeseries = dict()
    data_path = analysis_parameters.DIR_PROCESSED_DATA
    # Read in model data
    for experiment_id in THIS_EXPERIMENT_ID:
        filename = data_path + 'model_data/modelData_tas_' + experiment_id + '.zarr'
        data = xr.open_zarr(filename)
        dict_timeseries[experiment_id] = data
    # Read in observation data
    filename = data_path + 'observation_data/historical_obs.zarr'
    data = xr.open_zarr(filename)
    dict_timeseries['historical_obs'] = data

    return dict_timeseries


def create_country2city2latlon_dict():
    """Creates a country-city, latitude-longitude dictionary.

    Returns a nested dictionary. First key is country. Second Key is city.
    The value is the lat lon value that will be used to update the timeseries
    plot. The first key will be a drop down menu and the second will be a drop
    down menu that depends on the input of the first.

    Returns:
        my_dict: The city latitude-longitude dictionary.
    """
    my_dict = dict()
    for country in COUNTRIES:
        my_dict.update({country: dict()})
    for i in range(12959):
        coun = DF['country'].values[i]
        city = DF['city_ascii'].values[i]
        lat = DF['lat'].values[i]
        lon = DF['lng'].values[i]
        latlon = [lat, lon]
        my_dict[coun].update({city: latlon})

    return my_dict
