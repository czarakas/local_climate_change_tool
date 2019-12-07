"""
Unit tests for subcomponent d
"""
import math
import sys
import datetime as dt
from netCDF4 import Dataset
import xarray as xr
import pandas as pd
import numpy as np
import glob

sys.path.append(".")

import data_wrangler as dw
import analysis_parameters as params
import subcomp_d_process_historical_obs as process_obs


TEST_DATA_DIR = params.DIR_INTERMEDIATE_OBSERVATION_DATA
TEST_OUTPUT_DIR = params.DIR_TESTING_DATA
TEST_FILE = TEST_DATA_DIR + 'Complete_TAVG_LatLong1.nc'
OUTPUT_FILE_NAME = 'historical_obs.zarr'
OUTPUT_FILE = TEST_OUTPUT_DIR + OUTPUT_FILE_NAME

# expected types and dimensions of processed obs dataset (latitude, longitude, time)
EXP_TYPES = np.array([xr.core.dataset.Dataset, np.float32, np.float64, np.datetime64])
EXP_DIMS = [180, 360, 2037]


def test_convert_to_360():
    """
    Tests if the convert_to_360 function correctly converts -180 to 180 longitudes to
    0 to 360 longitudes.
    """
    test_lons = [-180., 180., 0., 360., -135., 135.]
    exp_lons = [180., 180., 0., 360., 225., 135.]
    
    conv_lons = process_obs.convert_to_360(test_lons)
    
    assert np.array_equal(exp_lons, conv_lons)


def test_calculate_temps():
    """
    Tests that the raw observations file exists and calculate_temps function returns a list 
    of length 4 with t_avg, time, and lat and lon with the expected data types.
    """
    output = process_obs.calculate_temps(filename=TEST_FILE)
    exp_length = 4
    exp_types = [np.ndarray, pd.core.indexes.datetimes.DatetimeIndex, 
                      np.ndarray, np.ndarray]
    
    correct_length = len(output) == exp_length
    if correct_length:
        correct_types = all([isinstance(output[i], exp_types[i]) for i in range(exp_length)])
    else:
        correct_types = False
        
    assert correct_types
    assert correct_length


def test_create_obs_dataset():
    """
    Tests that the create_obs_dataset function returns a dataset with the expected types and
    dimensions.
    """
    [t_avg, time, lat, lon] = process_obs.calculate_temps(filename=TEST_FILE)
    test_ds = process_obs.create_obs_dataset(t_avg, time, lat, lon)
    test_coords = [x for x in test_ds.coords]
    
    ds_pass = isinstance(test_ds, EXP_TYPES[0])
    lat_pass = (isinstance(test_ds['lat'].values[0], EXP_TYPES[1]) and len(test_ds['lat'].values) == EXP_DIMS[0])
    lon_pass = (isinstance(test_ds['lon'].values[0], EXP_TYPES[2]) and len(test_ds['lon'].values) == EXP_DIMS[1])
    time_pass = (isinstance(test_ds['time'].values[0], EXP_TYPES[3]) and len(test_ds['time'].values) == EXP_DIMS[2])

    assert ds_pass
    assert lat_pass
    assert lon_pass
    assert time_pass


def test_save_dataset(): 
    """
    Tests that the dataset was saved correctly and looks the same as the processed dataset.
    """
    # first delete the file if it already exists in the directory - zarr can't overwrite
    dw.delete_zarr_files(data_dir=TEST_OUTPUT_DIR, regex=OUTPUT_FILE_NAME, file_type='')

    process_obs.process_all_observations(data_path=TEST_DATA_DIR,
                                        data_path_out=TEST_OUTPUT_DIR)

    out_dir_files = glob.glob(TEST_OUTPUT_DIR + '*.zarr', recursive=True)
    file_exists = OUTPUT_FILE in out_dir_files

    if file_exists:
        test_ds = xr.open_zarr(OUTPUT_FILE)
        test_coords = [x for x in test_ds.coords]

        ds_pass = isinstance(test_ds, EXP_TYPES[0])
        lat_pass = (isinstance(test_ds['lat'].values[0], EXP_TYPES[1]) and len(test_ds['lat'].values) == EXP_DIMS[0])
        lon_pass = (isinstance(test_ds['lon'].values[0], EXP_TYPES[2]) and len(test_ds['lon'].values) == EXP_DIMS[1])
        time_pass = (isinstance(test_ds['time'].values[0], EXP_TYPES[3]) and len(test_ds['time'].values) == EXP_DIMS[2])
    else:
        ds_pass = False
        lat_pass = False
        lon_pass = False
        time_pass = False

    assert file_exists
    assert ds_pass
    assert lat_pass
    assert lon_pass
    assert time_pass


def main():
    """Runs all tests for each of the functions in the subcomp_d module."""
    test_convert_to_360()
    test_calculate_temps()
    test_create_obs_dataset()
    test_save_dataset()


if __name__ == '__main__':
    main()