'''
util_panel.py
Sami Turbeville
CSE 583 Project: CMIP 6 Local Climate Tool

Module of useful functions for creating panel
'''

import pandas as pd
import zarr
import xarray as xr
import sys

dir_analysis = '/home/jovyan/local-climate-data-tool/Analysis/Phase1_ProcessData'
sys.path.insert(0, dir_analysis)
import analysis_parameters


DF = pd.read_csv('worldcities.csv')
COUNTRIES = list(set(DF['country']))
DATA_PATH = analysis_parameters.DIR_DUMMY_DATA
THIS_EXPERIMENT_ID = ['historical','ssp126', 'ssp370','ssp245','ssp585']
EXPERIMENT_KEYS = THIS_EXPERIMENT_ID.copy()
EXPERIMENT_KEYS.append('historical_obs')

def read_data():
    ''' Returns a dictionary with keys: 
            historical
            ssp126
            ssp370
            ssp245
            ssp585
            historical_obs
    '''
    #initiate dictionary - which will match experiment names to data
    dict_timeseries = dict()
    
    # Read in model data
    for experiment_id in THIS_EXPERIMENT_ID:
        filename = DATA_PATH + 'Zarr/dummyData_modelData_' + experiment_id + '.zarr'
        ds = xr.open_zarr(filename)
        dict_timeseries[experiment_id] = ds

    # Read in observation data
    filename = DATA_PATH + 'Zarr/dummyData_observationData' + '.zarr'
    ds = xr.open_zarr(filename)
    dict_timeseries['historical_obs'] = ds
    return dict_timeseries

def create_country2city2latlon_dict():
    '''
    Returns a nested dictionary. First key is country.
        Second Key is city. The value is the lat lon 
        value that will be used to update the timeseries
        plot. The first key will be a drop down menu and 
        the second will be a drop down menu that depends 
        on the input of the first. 
    '''
    my_dict = dict()
    for country in COUNTRIES:
        my_dict.update({country : dict()})
    for i in range(12959):
        coun = DF['country'].values[i]
        city = DF['city_ascii'].values[i]
        lat = DF['lat'].values[i]
        lon = DF['lng'].values[i]
        latlon = [lat, lon]        
        my_dict[coun].update({city : latlon})
    return my_dict