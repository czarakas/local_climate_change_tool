"""
test_subcomp_c.py

Contains the test class for subcomp_c_multi_model_stats.py.
"""
import time
import glob
import unittest
import cftime
import pandas as pd
import xarray as xr
import numpy as np

from phase1_data_wrangler.analysis_parameters import \
    DIR_TESTING_DATA, VARIABLE_ID
from phase1_data_wrangler.subcomp_c_multi_model_stats import \
    initialize_empty_mms_arrays, fill_empty_arrays, create_xr_dataset, \
    get_scenario_fnames, read_in_fname

DATA_PATH = DIR_TESTING_DATA+'processed_model_data/'
SCENARIO = 'historical'
FNAME_TEST = 'tas_historical_CAMS-CSM1-0'
VARIABLE_NAME = VARIABLE_ID
NORMALIZED = False
NUM_CHUNKS = 20
EXP_TYPES = np.array([xr.core.dataarray.DataArray,
                      np.ndarray,
                      np.float64,
                      cftime._cftime.DatetimeProlepticGregorian])

[EMPTY_DSETS,
 DIM_INFO, DIMS,
 FILE_NAMES,
 DATASETS] = initialize_empty_mms_arrays(data_path=DATA_PATH, scenario_name=SCENARIO,
                                         num_chunks=NUM_CHUNKS, normalized=NORMALIZED)
[LATS, LONS, TIMES] = DIMS

[MULTI_MODEL_MEANS,
 MULTI_MODEL_MINS,
 MULTI_MODEL_MAXS,
 MULTI_MODEL_STDS] = fill_empty_arrays(empty_dsets=EMPTY_DSETS, dim_info=DIM_INFO,
                                       file_names=FILE_NAMES, datasets=DATASETS,
                                       varname=VARIABLE_NAME, num_chunks=NUM_CHUNKS)

DS = create_xr_dataset(lats=LATS, lons=LONS, times=TIMES,
                       mean_vals=MULTI_MODEL_MEANS, max_vals=MULTI_MODEL_MAXS,
                       min_vals=MULTI_MODEL_MINS, std_vals=MULTI_MODEL_STDS)

#----------------------------------------------------------------------------------
def check_coord_names(ds_processed, ds_coords_expected):
    """Checks whether coordinate names of ds are expected names."""
    coords_list = []
    for coord in ds_processed.coords:
        coords_list.append(coord)
    return bool(set(coords_list) == set(ds_coords_expected))


def check_years(ds_processed, min_year, max_year):
    """Check that times are within range of plausible years for the output."""
    first_date = ds_processed['time'].values[0]
    if isinstance(first_date, np.datetime64):
        first_yr = pd.to_datetime(first_date).year
    else:
        first_yr = first_date.year
    if first_yr > min_year:
        if first_yr < max_year:
            return True
        else:
            print('Start year is too big')
            return False
    else:
        print('Start year is too small')
        return False


def check_coord_types(ds_processed, expected_types):
    """
    Checks that processed dataset consists of coordinates
    of expected data types.
    """
    [exp_type_dim, exp_type_dim_value, exp_type_latlon, exp_type_time] = expected_types

    time_types_pass = (isinstance(ds_processed['time'].values[0], exp_type_time) and
                       isinstance(ds_processed['time'], exp_type_dim) and
                       isinstance(ds_processed['time'].values, exp_type_dim_value))

    lat_types_pass = (isinstance(ds_processed['lat'].values[0], exp_type_latlon) and
                      isinstance(ds_processed['lat'], exp_type_dim) and
                      isinstance(ds_processed['lat'].values, exp_type_dim_value))

    lon_types_pass = (isinstance(ds_processed['lon'].values[0], exp_type_latlon) and
                      isinstance(ds_processed['lon'], exp_type_dim) and
                      isinstance(ds_processed['lon'].values, exp_type_dim_value))

    return bool(time_types_pass and lat_types_pass and lon_types_pass)


class TestSubcompC(unittest.TestCase):
    """Test class for subcomp_c_multi_model_stats.py."""

    def test_fname_list(self, data_path=DATA_PATH, scenario=SCENARIO, normalized=NORMALIZED):
        """
        Tests that filename list generation actually generates a list of more
        than one filename and that the filenames are strings.
        """
        names = get_scenario_fnames(data_path, scenario, normalized)

        more_than_one_fname = bool(len(names) > 0)

        correct_type = isinstance(names[0], str)

        self.assertTrue(more_than_one_fname and correct_type)

    def test_read_in_fname(self, data_path=DATA_PATH, fname=FNAME_TEST, expected_types=EXP_TYPES):
        """
        Checks that the file name is read in correctly and its contents
        are as expected.
        """
        ds = read_in_fname(data_path=DATA_PATH, fname=FNAME_TEST)

        file_exists = ds is not None

        coord_names_pass = check_coord_names(ds, ds_coords_expected=['time', 'lon', 'lat'])

        # Check that coordinate types are right
        coord_types_pass = check_coord_types(ds, expected_types)

        # Check that time is reasonable (e.g. )
        years_pass = check_years(ds, min_year=1849, max_year=2200)

        self.assertTrue(file_exists and coord_names_pass and years_pass)

    def test_initialize_empty_mms_arrays(self, data_path=DATA_PATH, scenario_name=SCENARIO,
                                         num_chunks=NUM_CHUNKS, normalized=NORMALIZED):
        """Tests that the arrays were initialized."""
        [empty_dsets,
         dim_info, dims,
         file_names,
         datasets] = initialize_empty_mms_arrays(data_path, scenario_name, num_chunks, normalized)

        files_exist = empty_dsets is not None

        self.assertTrue(files_exist)

    def test_fill_empty_arrays(self, empty_dsets=EMPTY_DSETS, dim_info=DIM_INFO,
                               file_names=FILE_NAMES, datasets=DATASETS,
                               varname=VARIABLE_NAME, num_chunks=NUM_CHUNKS):
        """
        Tests that the multi-model statistics do not contain nans and
        that min < mean < max.
        """
        time_ind = 0
        lat_ind = 0
        lon_ind = 0

        [multi_model_means,
         multi_model_mins,
         multi_model_maxs,
         multi_model_stds] = fill_empty_arrays(empty_dsets, dim_info, file_names,
                                               datasets, varname, num_chunks)

        no_nans = ((not np.isnan(multi_model_means).any()) and
                   (not np.isnan(multi_model_mins).any()) and
                   (not np.isnan(multi_model_maxs).any()) and
                   (not np.isnan(multi_model_stds).any()))

        logical_val_order = ((multi_model_means[time_ind, lat_ind, lon_ind] <=
                              multi_model_maxs[time_ind, lat_ind, lon_ind]) and
                             (multi_model_means[time_ind, lat_ind, lon_ind] >=
                              multi_model_mins[time_ind, lat_ind, lon_ind]))

        self.assertTrue(no_nans and logical_val_order)

    def test_create_xr_dataset(self, dims=DIMS, mean_vals=MULTI_MODEL_MEANS,
                               max_vals=MULTI_MODEL_MAXS, min_vals=MULTI_MODEL_MINS,
                               std_vals=MULTI_MODEL_STDS):
        """Tests that the dataset exists after it was created."""
        [lats, lons, times] = dims
        ds = create_xr_dataset(lats, lons, times, mean_vals, max_vals, min_vals, std_vals)

        self.assertTrue(ds is not None)


if __name__ == '__main__':
    unittest.main()
