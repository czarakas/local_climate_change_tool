"""
Add docstring
"""

# Import modules
import datetime
import cftime
import xarray as xr
import numpy as np

#import analysis_parameters
#import subcomp_a_create_data_dict
import subcomp_a_process_climate_model_data as process_data

# Define directory and file names
TEST_KEY1 = 'ScenarioMIP.MOHC.UKESM1-0-LL.ssp585.Amon.gn'
TEST_KEY2 = 'CMIP.CAMS.CAMS-CSM1-0.historical.Amon.gn'
TESTING_DATA_DIR = '/home/jovyan/local-climate-data-tool/Data/files_for_testing/'
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

def test_reindex_time():
    """Tests whether the reindex_time function works as expected"""
    [yr, month, day] = [1850, 1, 15]
    testdates1 = xr.DataArray(np.array([np.datetime64(datetime.datetime(yr, month, day, 0, 0)),
                                        np.datetime64(datetime.datetime(yr, month+1, day, 0, 0))]))
    testdates2 = xr.DataArray(np.array([cftime.DatetimeNoLeap(yr, month, day, 0, 0),
                                        cftime.DatetimeNoLeap(yr, month+1, day, 0, 0)]))
    testdates3 = xr.DataArray(np.array([cftime.Datetime360Day(yr, month, day, 0, 0),
                                        cftime.Datetime360Day(yr, month+1, day, 0, 0)]))
    dates_to_test = [testdates1, testdates2, testdates3]

    # Run test
    for date_to_test in dates_to_test:
        newtimes = process_data.reindex_time(date_to_test)
       # print(newtimes)

    assert True

def test_generate_new_filename(test_key=TEST_KEY1):
    """Test that the generate_new_filename function generates a string"""
    fname = process_data.generate_new_filename(test_key)
    assert ((fname is not None) and (type(fname) == str))

def test_create_reference_grid(dset_dict=DSET_DICT, test_key=TEST_KEY2):
    """ Tests that the reference grid function creates a sensible reference grid"""
    ds_original = dset_dict[test_key]
    ds_ref_grid = process_data.create_reference_grid(dset_dict=dset_dict,
                                                     reference_key=test_key)

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

    assert (correct_dim_size and no_extra_vars and no_nans and one_dim and big_enough)


def test_regrid_model(dset_dict=DSET_DICT, key_to_regrid=TEST_KEY1,
                      key_for_grid=TEST_KEY2, varname=VARNAME):
    """Tests that the regrid function works"""
    ds_to_regrid = dset_dict[key_to_regrid]
    reference_grid = process_data.create_reference_grid(dset_dict=dset_dict,
                                                        reference_key=key_for_grid)

    ########### REGRID
    ds_regridded = process_data.regrid_model(ds_to_regrid,
                                             reference_grid)

    # Check that regridded data actually aligns with reference grid
    print(np.size(ds_regridded['lat'].values) == np.size(reference_grid['lat'].values))
    print(np.size(ds_regridded['lon'].values) == np.size(reference_grid['lon'].values))

    # Check that time dimensions have not changed
    print(ds_regridded['time'].values == ds_to_regrid['time'].values)

    # Check that there aren't nans if there weren't in original array
    if not np.isnan(ds_to_regrid[varname].values).any():
        assert not np.isnan(ds_regridded[varname].values).any()
    else:
        assert True
        print('NANs were in original array')

def test_process_dataset(dset_dict=DSET_DICT,
                         key_to_process=TEST_KEY1,
                         key_for_grid=TEST_KEY2,
                         test_inds=TEST_INDS,
                         expected_types=EXP_TYPES):
    """Tests whether the processed dataset output by the process_dataset
    function has expected coordinates and dimensions and plausible values"""
    #------------------ Process test dataset------------------------------------
    ds_original = dset_dict[key_to_process]
    ds_ref_grid = process_data.create_reference_grid(dset_dict=dset_dict,
                                                     reference_key=key_for_grid)
    ds_processed = process_data.process_dataset(this_key=key_to_process,
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

    # !!!!!!!!!!!!! NEED TO DO Check that it actually averaged over all ensemble members

    assert coord_names_pass and years_pass and dims_pass and coord_types_pass

    
def check_coord_names(ds_processed, ds_coords_expected):
    """Checks whether coordinate names of ds are expected names"""
    coords_list = []
    for coord in ds_processed.coords:
        coords_list.append(coord)
    return bool(set(coords_list) == set(ds_coords_expected))

def check_dims(ds_processed, ds_original, ds_ref_grid):
    """Checks whether dimensions of dataset are expected based on
    regridding and original dataset dimensions"""
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
    """ Check that times are within range of plausible years for
    model output"""
    if ds_processed['time'].values[0].year > min_year:
        if ds_processed['time'].values[0].year < max_year:
            return True
        else:
            print('Start year is too big')
            return False
    else:
        print('Start year is too small')
        return False

def check_coord_types(ds_processed, expected_types):
    """Checks that processed dataset consists of coordinates
    of expected data types"""
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
