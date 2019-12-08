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
import unittest

sys.path.append(".")

import data_wrangler as dw
import analysis_parameters as params
import subcomp_d_process_historical_obs as process_obs


TEST_DATA_DIR = params.DIR_INTERMEDIATE_OBSERVATION_DATA
TEST_OUTPUT_DIR = params.DIR_TESTING_DATA + 'dummy_obs_data/'
TEST_FILE = TEST_DATA_DIR + 'Complete_TAVG_LatLong1.nc'
OUTPUT_FILE_NAME = 'dummy_test_dataset.zarr'
OUTPUT_FILE = TEST_OUTPUT_DIR + OUTPUT_FILE_NAME

# expected types and dimensions of processed obs dataset (latitude, longitude, time)
EXP_TYPES = np.array([xr.core.dataset.Dataset,
                      np.float32,
                      np.float64,
                      np.datetime64])
EXP_DIMS = [180, 360, 2037]

# dummy Dataset to test if the file saves correctly
DUMMY_VAR = xr.DataArray()
DUMMY_OBS = xr.Dataset(data_vars={'mean': (['time', 'lat', 'lon'],
                                           np.empty((2, 2, 2)))},
                             coords={'time': [0, 1],
                                     'lat': [0, 1],
                                     'lon':[0, 1]})

class test_subcomp_d(unittest.TestCase):
    def test_convert_to_360(self):
        """
        Tests if the convert_to_360 function correctly converts -180 to 180
        longitudes to 0 to 360 longitudes.
        """
        test_lons = [-180., 180., 0., 360., -135., 135.]
        exp_lons = [180., 180., 0., 360., 225., 135.]

        conv_lons = process_obs.convert_to_360(test_lons)

        self.assertTrue(np.array_equal(exp_lons, conv_lons))


    def test_calculate_temps(self):
        """
        Tests that the raw observations file exists and calculate_temps function
        returns a list of length 4 with t_avg, time, and lat and lon with the
        expected data types.
        """
        output = process_obs.calculate_temps(filename=TEST_FILE)
        exp_length = 4
        exp_types = [np.ndarray, pd.core.indexes.datetimes.DatetimeIndex, 
                          np.ndarray, np.ndarray]

        correct_length = len(output) == exp_length
        if correct_length:
            correct_types = all([isinstance(output[i], exp_types[i])
                                 for i in range(exp_length)])
        else:
            correct_types = False

        self.assertTrue(correct_types)
        self.assertTrue(correct_length)


    def test_create_obs_dataset(self):
        """
        Tests that the create_obs_dataset function returns a dataset with the expected types and
        dimensions.
        """
        [t_avg, time, lat, lon] = process_obs.calculate_temps(filename=TEST_FILE)
        test_ds = process_obs.create_obs_dataset(t_avg, time, lat, lon)
        test_coords = [x for x in test_ds.coords]

        ds_pass = isinstance(test_ds, EXP_TYPES[0])
        lat_pass = (isinstance(test_ds['lat'].values[0], EXP_TYPES[1]) and
                    len(test_ds['lat'].values) == EXP_DIMS[0])
        lon_pass = (isinstance(test_ds['lon'].values[0], EXP_TYPES[2]) and
                    len(test_ds['lon'].values) == EXP_DIMS[1])
        time_pass = (isinstance(test_ds['time'].values[0], EXP_TYPES[3])and
                     len(test_ds['time'].values) == EXP_DIMS[2])

        self.assertTrue( ds_pass)
        self.assertTrue( lat_pass)
        self.assertTrue( lon_pass)
        self.assertTrue( time_pass)


    def test_save_dataset(self): 
        """Tests that the dataset was saved correctly."""
        # if the directory is not empty, delete first - zarr can't overwrite
        dw.delete_zarr_files(data_dir=TEST_OUTPUT_DIR, regex='',
                             file_type=OUTPUT_FILE_NAME)

        process_obs.save_dataset(best_data=DUMMY_OBS,
                                 data_path_out=TEST_OUTPUT_DIR,
                                 out_file_name=OUTPUT_FILE_NAME)

        out_dir_files = glob.glob(TEST_OUTPUT_DIR + '*.zarr', recursive=True)
        file_exists = OUTPUT_FILE in out_dir_files

        if file_exists:
            test_ds = xr.open_zarr(OUTPUT_FILE)

            ds_pass = isinstance(test_ds, type(DUMMY_OBS))
            var_pass = np.array_equal(test_ds['mean'], DUMMY_OBS['mean'])
            coord_pass = ((test_ds.lat.values == DUMMY_OBS.lat.values).all() and
                          (test_ds.lon.values == DUMMY_OBS.lon.values).all() and
                          (test_ds.time.values == DUMMY_OBS.time.values).all())
        else:
            ds_pass = False
            var_pass = False
            coord_pass = False

        self.assertTrue( file_exists)
        self.assertTrue( ds_pass)
        self.assertTrue( var_pass)
        self.assertTrue( coord_pass)

#     def test_process_all_observations(self):
#         """add docstring"""
#         # first delete the file if it already exists in the directory;
#         # zarr can't overwrite
#         dw.delete_zarr_files(data_dir=TEST_OUTPUT_DIR,
#                              regex=OUTPUT_FILE_NAME, file_type='')
        
        

    
if __name__ == '__main__':
    unittest.main()
