"""
test_subcomp_b.py

Contains the test class for subcomp_b_process_climate_model_data.py.
"""
import datetime
import cftime
import unittest
import os
import glob
import pandas as pd
import xarray as xr
import numpy as np

from phase1_data_wrangler.subcomp_b_process_climate_model_data import \
    reindex_time, generate_new_filename, create_reference_grid, \
    regrid_model, process_dataset, process_all_files_in_dictionary
from phase1_data_wrangler.analysis_parameters import DIR_TESTING_DATA
import download_file_from_google_drive

# Download files
download_file_from_google_drive.download_data_predefined('Files_for_Testing')

# Define directory and file names
TEST_KEY1 = 'ScenarioMIP.MOHC.UKESM1-0-LL.ssp585.Amon.gn'
TEST_KEY2 = 'CMIP.CAMS.CAMS-CSM1-0.historical.Amon.gn'

TESTING_DATA_DIR = DIR_TESTING_DATA+'raw_data/'
TESTING_OUTPUT_DIR = DIR_TESTING_DATA+'processed_model_data/'
VARNAME = 'tas'
TEST_INDS = [44, 120, 0]
EXP_TYPES = np.array([xr.core.dataarray.DataArray,
                      np.ndarray,
                      np.float64,
                      cftime._cftime.DatetimeProlepticGregorian])

# Read testing data into dictionary
DSET_DICT = dict()
DSET_DICT[TEST_KEY1] = xr.open_dataset(TESTING_DATA_DIR+TEST_KEY1+'.nc')
DSET_DICT[TEST_KEY2] = xr.open_dataset(TESTING_DATA_DIR+TEST_KEY2+'.nc')

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

def check_coord_names(ds_processed, ds_coords_expected):
    """Checks whether the coordinate names of ds are expected names."""
    coords_list = []
    for coord in ds_processed.coords:
        coords_list.append(coord)
    return bool(set(coords_list) == set(ds_coords_expected))


def check_dims(ds_processed, ds_original, ds_ref_grid):
    """
    Checks whether dimensions of dataset are expected based on
    regridding and original dataset dimensions.
    """
    if ds_processed.dims['time'] == ds_original.dims['time']:
        if  ds_processed.dims['lat'] == ds_ref_grid.dims['lat']:
            if ds_processed.dims['lon'] == ds_ref_grid.dims['lon']:
                return True
            else:
                print('Incorrect lon dimension')
                return False
        else:
            print('Incorrect lat dimension')
            return False
    else:
        print('Incorrect time dimension')
        return False


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

    lat_types_pass = (isinstance(ds_processed['lat'].values[0], exp_type_latlon) and
                      isinstance(ds_processed['lat'], exp_type_dim) and
                      isinstance(ds_processed['lat'].values, exp_type_dim_value))

    lon_types_pass = (isinstance(ds_processed['lon'].values[0], exp_type_latlon) and
                      isinstance(ds_processed['lon'], exp_type_dim) and
                      isinstance(ds_processed['lon'].values, exp_type_dim_value))

    return bool(lat_types_pass and lon_types_pass)


def delete_zarr_files(data_dir, regex):
    """Deletes zarr files matching regular expression.

    This is a necessary function because zarr files cannot be overwritten.

    Args:
        data_dir: The directory containing the files to be deleted.
        regex: String (e.g. 'filename*') matching the files to be deleted.
    """
    i = 0
    for file in glob.glob(data_dir+regex+'.zarr'):
        os.system('rm -rf '+file)
        i = i+1
    print('deleted '+str(i)+' files in '+data_dir)


class TestSubcompB(unittest.TestCase):
    """Test class for subcomp_b_process_climate_model_data.py"""

    def test_reindex_time(self):
        """Tests whether the reindex_time function works as expected."""
        [yr, month, day] = [1850, 1, 15]
        expected_times = xr.DataArray(np.array([cftime.DatetimeProlepticGregorian(yr, month, day, 0, 0),
                                                cftime.DatetimeProlepticGregorian(yr, month+1, day, 0, 0)]))
        testdates1 = xr.DataArray(np.array([np.datetime64(datetime.datetime(yr, month, day, 0, 0)),
                                            np.datetime64(datetime.datetime(yr, month+1, day, 0, 0))]))
        testdates2 = xr.DataArray(np.array([cftime.DatetimeNoLeap(yr, month, day, 0, 0),
                                            cftime.DatetimeNoLeap(yr, month+1, day, 0, 0)]))
        testdates3 = xr.DataArray(np.array([cftime.Datetime360Day(yr, month, day, 0, 0),
                                            cftime.Datetime360Day(yr, month+1, day, 0, 0)]))
        dates_to_test = [testdates1, testdates2, testdates3]

        # Run test
        dates_converted = True
        for date_to_test in dates_to_test:
            newtimes = reindex_time(date_to_test)
            if not np.all((newtimes == expected_times).values):
                dates_converted = False
            else:
                continue
        self.assertTrue(dates_converted)

    def test_generate_new_filename(self, test_key=TEST_KEY1):
        """Tests that the generate_new_filename function generates a string."""
        fname = generate_new_filename(test_key)
        self.assertTrue(((fname is not None) and (type(fname) == str)))

    def test_create_reference_grid(self, dset_dict=DSET_DICT, test_key=TEST_KEY2):
        """Tests that the reference grid function creates a sensible reference grid."""
        ds_original = dset_dict[test_key]
        ds_ref_grid = create_reference_grid(dset_dict=dset_dict, reference_key=test_key)

        # Check that latitude and longitude dimensions haven't changed in regridding
        correct_dim_size = ((ds_original.dims['lat'] == ds_ref_grid.dims['lat']) and
                            (ds_original.dims['lon'] == ds_ref_grid.dims['lon']))

        # Check that reference grid doesn't have any variables other than lat and lon
        no_extra_vars = (len(ds_ref_grid.variables) == 2)

        # Check that latitude and longitude coordinates do not contain nans
        no_nans = ((not np.isnan(ds_ref_grid['lat'].values).any()) and
                   (not np.isnan(ds_ref_grid['lon'].values).any()))

        #Check that latitude and longitude arrays are 1D
        one_dim = ((np.size(ds_ref_grid['lat'].values) == np.shape(ds_ref_grid['lat'].values)[0]) and
                   (np.size(ds_ref_grid['lon'].values) == np.shape(ds_ref_grid['lon'].values)[0]))

        # Check that latitude and longitude arrays are big enough
        min_coord_size = 20
        big_enough = ((np.size(ds_ref_grid['lat'].values) > min_coord_size) and
                      (np.size(ds_ref_grid['lon'].values) > min_coord_size))

        self.assertTrue(correct_dim_size)
        self.assertTrue(no_extra_vars)
        self.assertTrue(no_nans)
        self.assertTrue(one_dim)
        self.assertTrue(big_enough)

    def test_regrid_model_dims(self, dset_dict=DSET_DICT, key_to_regrid=TEST_KEY1,
                               key_for_grid=TEST_KEY2):
        """Tests that the regrid function results in an array of the right dimensions."""

        # Regrid model output
        ds_to_regrid = dset_dict[key_to_regrid]
        reference_grid = create_reference_grid(dset_dict=dset_dict, reference_key=key_for_grid)
        ds_regridded = regrid_model(ds_to_regrid, reference_grid)

        # Check that lat/lonregridded data actually aligns with reference grid
        correct_lat_dim = np.size(ds_regridded['lat'].values) == np.size(reference_grid['lat'].values)
        correct_lon_dim = np.size(ds_regridded['lon'].values) == np.size(reference_grid['lon'].values)

        # Check that time dimensions have not changed
        correct_time_dim = np.equal(ds_regridded['time'].values, ds_to_regrid['time'].values).all()
        self.assertTrue(correct_lat_dim and correct_lon_dim and correct_time_dim)

    def test_regrid_model_nans(self, dset_dict=DSET_DICT, key_to_regrid=TEST_KEY1,
                               key_for_grid=TEST_KEY2, varname=VARNAME):
        """Tests that the regrid function doesn't create any nans."""
        ds_to_regrid = dset_dict[key_to_regrid]
        reference_grid = create_reference_grid(dset_dict=dset_dict, reference_key=key_for_grid)
        ds_regridded = regrid_model(ds_to_regrid, reference_grid)

        # Check that there aren't nans if there weren't in original array
        if np.isnan(ds_to_regrid[varname].values).any():
            raise ValueError('NANs were in original array')
        else:
            self.assertTrue(not np.isnan(ds_regridded[varname].values).any())

    def test_process_dataset(self,
                             dset_dict=DSET_DICT,
                             key_to_process=TEST_KEY1,
                             key_for_grid=TEST_KEY2,
                             test_inds=TEST_INDS,
                             expected_types=EXP_TYPES):
        """
        Tests whether the processed dataset output by the process_dataset
        function has expected coordinates and dimensions and plausible values.
        """
        #------------------ Process test dataset------------------------------------
        ds_original = dset_dict[key_to_process]
        ds_ref_grid = create_reference_grid(dset_dict=dset_dict,
                                            reference_key=key_for_grid)
        ds_processed = process_dataset(this_key=key_to_process,
                                       dset_dict=dset_dict,
                                       final_grid=ds_ref_grid)

        #------------------ Run tests on processed dataset-------------------------
        # Check that lat/lon/time coordinate names are right
        coord_names_pass = check_coord_names(ds_processed, ds_coords_expected=['time', 'lon', 'lat'])

        # Check that time is reasonable (e.g. )
        years_pass = check_years(ds_processed, min_year=1849, max_year=2200)

        # Check that lat, lon, and time dimensions are what we expect
        dims_pass = check_dims(ds_processed, ds_original, ds_ref_grid)

        # Check that coordinate types are right
        coord_types_pass = check_coord_types(ds_processed, expected_types)

        self.assertTrue(coord_names_pass)
        self.assertTrue(years_pass)
        self.assertTrue(dims_pass)
        self.assertTrue(coord_types_pass)

    def test_save_dataset(self,
                          dset_dict=DSET_DICT,
                          data_path_out=TESTING_OUTPUT_DIR,
                          key_for_grid=TEST_KEY2,
                          exceptions_list=(),
                          expected_types=EXP_TYPES):
        """Tests that the datasets save correctly."""
        final_grid = create_reference_grid(dset_dict=dset_dict,
                                           reference_key=key_for_grid)

        delete_zarr_files(data_dir=data_path_out, regex='*')

        process_all_files_in_dictionary(dset_dict, exceptions_list,
                                        final_grid, data_path_out)
        endcut = -1*len('.zarr')
        begcut = len(data_path_out)
        names = [f[begcut:endcut] for f in glob.glob(data_path_out +'*.zarr')]
        files_are_saved = bool(len(names) > 0)

        coord_names_pass = True
        years_pass = True
        coord_types_pass = True
        for fname in names:
            filename = data_path_out + fname + '.zarr'
            ds = xr.open_zarr(filename)
            ds = xr.decode_cf(ds)

            # Check that ds looks the same as the processed dataset
            coord_names_pass = coord_names_pass and check_coord_names(ds, ds_coords_expected=['time', 'lon', 'lat'])
            coord_types_pass = coord_types_pass and check_coord_types(ds, expected_types)
            years_pass = years_pass and check_years(ds, min_year=1849, max_year=2200)

        self.assertTrue(files_are_saved)
        self.assertTrue(coord_names_pass)
        self.assertTrue(years_pass)
        self.assertTrue(coord_types_pass)


if __name__ == '__main__':
    unittest.main()
