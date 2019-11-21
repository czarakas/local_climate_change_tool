"""
Regrid the historical observations to be consistent with processed CMIP6 model
output.

*** WILL NOT RUN RIGHT NOW - need to correct the path to DATA_DIR ***

Author: Jacqueline Nugent
Last Modified: November 21, 2019
"""

from netCDF4 import Dataset
import xarray as xr
import glob
import pandas as pd
import math
import datetime as dt

import analysis_parameters

### TODO: that DATA_DIR is not defined!!!!!!!
DATA_DIR = analysis_parameters.DIR_INTERMEDIATE_PROCESSED_HISTORICAL_DATA
OUT_DIR = analysis_parameters.DIR_PROCESSED_DATA + 'observation_data/'


def read_netcdf_files(data_path):
    """
    Open all Complete_<var>_LatLong1.nc observation files int the data_path.
    Returns a list of the file names in the order [TAVG, TMAX, TMIN].
    """
    files = glob.glob(data_path + 'Complete' + '*.nc')
    
    return files


def calculate_temps(files):
    """
    Converts the temperature anomalies and climatologies from the
    observations into actual average, maximum, and minimum temperatures.
    Returns the average, maximum, and minimum temperatures and their
    dimensions (time, lat, lon) as a list of numpy arrays.
    """
    ### average monthly temperature:
    nc1 = Dataset(files[0], 'r')
    lat = nc1.variables['latitude'][:]
    lon = nc1.variables['longitude'][:]
    time_avg = nc1.variables['time'][:]
    t_avg_anom = nc1.variables['temperature'][:][:][:]
    t_avg_clima = nc1.variables['climatology'][:][:][:]

    ### maximum monthly temperature:
    nc2 = Dataset(files[1], 'r')
    time_max = nc2.variables['time'][:]
    t_max_anom = nc2.variables['temperature'][:][:][:]
    t_max_clima = nc1.variables['climatology'][:][:][:]

    ### minimum monthly temperature:
    nc3 = Dataset(files[2], 'r')
    time_min = nc3.variables['time'][:]
    t_min_anom = nc3.variables['temperature'][:][:][:]
    t_min_clima = nc1.variables['climatology'][:][:][:]
    
    ### skip the time steps that are in the average file but not min or max:
    nskip = len(time_avg)-len(time_min)
    new_t_avg_anom = t_avg_anom[nskip:, :, :]

    ### convert native time variables (in decimal year) to match model times
    [dec_start, yr_start] = math.modf(time_min[0])
    mnth_start = int(dec_start*12 + 1)
    first = dt.datetime(year=int(yr_start), month=mnth_start, day=15)

    [dec_end, yr_end] = math.modf(time_min[-1])
    mnth_end = int(dec_end*12 + 1)
    last = dt.datetime(year=int(yr_end), month=mnth_end, day=15)

    time = pd.date_range(start=first, end=last, periods=len(time_min))
    
    ### calculate the actual temperature statistics from the anomalies and
    ### climatologies:
    t_avg = np.empty(np.shape(new_t_avg_anom))
    t_max = np.empty(np.shape(t_max_anom))
    t_min = np.empty(np.shape(t_min_anom))

    for i in range(12):
        t_avg[i::12, :, :] = [(x + t_avg_clima[i, :, :]) 
                              for x in new_t_avg_anom[i::12, :, :]]
        t_max[i::12, :, :] = [(x + t_max_clima[i, :, :]) 
                              for x in t_max_anom[i::12, :, :]]
        t_min[i::12, :, :] = [(x + t_min_clima[i, :, :]) 
                              for x in t_min_anom[i::12, :, :]]
        
    return [t_avg, t_max, t_min, time, lat, lon]
    
    
def create_obs_dataset(t_avg, t_max, t_min, time, lat, lon):
    """
    Create a Dataset for the observations with variables tavg, tmax, and
    tmin in degrees C and dimensions time, lat, and lon. Arguments are
    the calculated average, maximum, and minimum temperatures returned
    by calc_temps() and the dimensions of the variables (time, lat, lon).
    """    
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

    ### create the Dataset
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
[t_avg, t_max, t_min, time, lat, lon] = calculate_temps(obs_file_names)
obs_ds = create_obs_dataset(t_avg, t_max, t_min, time, lat, lon)
save_dataset(obs_ds)
