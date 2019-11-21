"""
Regrid the historical observations to be consistent with processed CMIP6 model
output.

Author: Jacqueline Nugent
Last Modified: November 20, 2019
"""

from netCDF4 import Dataset
import xarray as xr
import glob
import pandas as pd
import math
import datetime as dt
import numpy as np 

import analysis_parameters


DATA_DIR = analysis_parameters.DIR_INTERMEDIATE_OBSERVATION_DATA
OUT_DIR = analysis_parameters.DIR_PROCESSED_DATA + 'observation_data/'


def read_netcdf_files(data_path):
    """
    Open all Complete_<var>_LatLong1.nc observation files int the data_path.
    Returns a list of the file names in the order [TAVG, TMAX, TMIN].
    """
    files = glob.glob(data_path + 'Complete' + '*.nc')
    
    return files


def create_obs_dataset(files):
    """
    Create a Dataset for the observations with variables tavg, tmax, and
    tmin in degrees C and dimensions time, lat, and lon.
    """
    ### average monthly temperature:
    nc1 = Dataset(files[0], 'r')
    lat = nc1.variables['latitude'][:]
    lon = nc1.variables['longitude'][:]
    time_dec = nc1.variables['time'][:]
    t_avg = nc1.variables['temperature'][:] 
    
    ### maximum monthly temperature:
    nc2 = Dataset(files[1], 'r')
    t_max = nc2.variables['temperature'][:]

    ### minimum monthly temperature
    nc3 = Dataset(files[2], 'r')
    t_min = nc3.variables['temperature'][:]

    ### convert native time variable (in decimal year) to match model times
    [dec_start, yr_start] = math.modf(time_dec[0])
    mnth_start = int(dec_start*12 + 1)
    first = dt.datetime(year=int(yr_start), month=mnth_start, day=15)
    
    [dec_end, yr_end] = math.modf(time_dec[-1])
    mnth_end = int(dec_end*12 + 1)
    last = dt.datetime(year=int(yr_end), month=mnth_end, day=15)
    
    time = pd.date_range(start=first, end=last, periods=len(time_dec))


    #### make data arrays for each variable 
    tavg = xr.DataArray(data=t_avg,
                             coords={'time': time, 'lat': lat, 'lon': lon},
                             dims=['time', 'lat', 'lon'])
    
    tmax = xr.DataArray(data=t_max,
                             coords={'time': time, 'lat': lat, 'lon': lon},
                             dims=['time', 'lat', 'lon'])
    
    tmin = xr.DataArray(data=t_min,
                             coords={'time': time, 'lat': lat, 'lon': lon},
                             dims=['time', 'lat', 'lon'])


    ### put them together as a dataset
    vardata = [tavg, tmax, tmin]
    varnames = ['tavg', 'tmax', 'tmin']
    var_dict = dict(zip(varnames, vardata))
    best_data = xr.Dataset(data_vars=var_dict)
    
    return best_data


def save_dataset(best):
    """Save the processed temperature observation Dataset to a zarr file"""
    best.load()
    best.chunk({'lat':10, 'lon':10, 'time':-1})
    best.to_zarr(OUT_DIR + 'historical_obs.zarr')


####### MAIN WORKFLOW ########

obs_file_names = read_netcdf_files(DATA_DIR)
obs_ds = create_obs_dataset(obs_file_names)
save_dataset(obs_ds)
