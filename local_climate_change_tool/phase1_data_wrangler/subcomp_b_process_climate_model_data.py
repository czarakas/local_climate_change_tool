"""
subcomp_b_process_climate_model_data.py

Processes raw CMIP6 output to create files with consistent dimensions for all models.
Running this script for all models with just averaging over ensembles, regridding,
and saving takes about 15-20 mins.

Make sure to clear the directory you would like the zarr files to be saved in - something about
this format makes it not work to overwrite existing files.
"""
import cftime
import xarray as xr
import xesmf as xe
import numpy as np

from phase1_data_wrangler.analysis_parameters import EXPERIMENT_LIST, \
    VARIABLE_ID, DIR_PROCESSED_DATA, DIR_INTERMEDIATE_PROCESSED_MODEL_DATA


THIS_EXPERIMENT_ID = EXPERIMENT_LIST
THIS_VARIABLE_ID = VARIABLE_ID
OUTPUT_PATH = DIR_PROCESSED_DATA
DIR_INTERMEDIATE = DIR_INTERMEDIATE_PROCESSED_MODEL_DATA


def create_reference_grid(reference_key, dset_dict):
    """Creates reference grid to which all model output will be regridded.

    Args:
        reference_key: The string key to the refefrence grid.
        dset_dict: The model data dictionary.
    Returns:
        ds_out: The dataset of the reference grid.
    """
    thisdata = dset_dict[reference_key]
    ds_out = xr.Dataset({'lat': thisdata['lat'],
                         'lon': thisdata['lon']})

    return ds_out


def reindex_time(startingtimes):
    """Reindexes time series to proleptic Gregorian calendar type.

    Args:
        startingtimes: Array of the time series.
    Returns:
        newtimes: Numpy array of the new, proleptic Gregorian calendar type times.
    """
    newtimes = np.empty(np.shape(startingtimes.values), dtype=cftime.DatetimeProlepticGregorian)
    for i in range(0, len(startingtimes)):
        yr = int(str(startingtimes.values[i])[0:4])
        mon = int(str(startingtimes.values[i])[5:7])
        newdate = cftime.DatetimeProlepticGregorian(yr, mon, 15)
        newtimes[i] = newdate

    return newtimes


def regrid_model(ds, reference_grid, latvariable='lat',
                 lonvariable='lon', regrid_method='nearest_s2d'):
    """Regrids model output to a reference grid.

    Args:
        ds: The dataset of the model output.
        reference_grid: The dataset containing the reference grid.
        latvariable: The string name for the latitude variable.
        lonvariable: The string name for the longitude variable.
        regrid_method: The string name of the method to use for regridding.
    Returns:
        data_series_regridded: The regridded model dataset.
    """
    data_series = ds[THIS_VARIABLE_ID]
    ds_in = xr.Dataset({'lat': data_series[latvariable],
                        'lon': data_series[lonvariable],
                        'time': data_series['time'],
                        THIS_VARIABLE_ID: data_series})
    regridder = xe.Regridder(ds_in, reference_grid, regrid_method, periodic=True)
    data_series_regridded = regridder(ds_in)
    data_series_regridded.attrs.update(data_series.attrs)

    return data_series_regridded


def process_dataset(this_key, dset_dict, final_grid):
    """Processes each dataset in dictionary.

    This processing involves:
        (1) Averaging over all ensemble members (member ids)
        (2) Getting into consistent time format
        (3) Renaming coordinates if necessary
        (4) Regridding to reference dataset

    Args:
        this_key: String key of the original datast in the dictionary.
        dset_dict: Dictionary of the model data.
        final_grid: Datasest of the final grid.
    Returns:
        dataset_regridded: The regridded model dataset.
    """
    # Get original dataset from dictionary
    ds_original = dset_dict[this_key]

    # Average over all ensemble members
    ds = ds_original.mean(dim=['member_id'])

    # Reindex time to consistent time datatype
    ds = xr.decode_cf(ds)
    newtimes = reindex_time(startingtimes=ds['time'])
    ds['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
    ds = ds.copy()

    # Rename latitude and longitude coordinate names if necessary
    if 'latitude' in ds.dims:
        ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
    else:
        pass

    # Regrid dataset to reference grid
    dataset_regridded = regrid_model(ds, final_grid)

    # If using a temperature variable, convert from K to C
    if THIS_VARIABLE_ID in ('tas', 'tasmin', 'tasmax'):
        dataset_regridded[THIS_VARIABLE_ID] = dataset_regridded[THIS_VARIABLE_ID] - 273.15

    return dataset_regridded


def generate_new_filename(this_key):
    """Generates filename for processed data from information in this_key."""
    [_, _, source_id, experiment_id, _, _] = this_key.split('.')
    this_fname = THIS_VARIABLE_ID+'_'+experiment_id+'_'+source_id
    return this_fname


def save_dataset(ds, this_fname, data_path):
    """Saves processed dataset ds as a zarr file: data_path/this_fname.zarr"""
    ds.load()
    # Export intermediate processed dataset as zarr file
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(data_path+this_fname+'.zarr')


##################### Main Workflow ##########################################

def process_all_files_in_dictionary(dset_dict, exceptions_list,
                                    final_grid, data_path_out=DIR_INTERMEDIATE):
    """Run process_dataset and save_dataset for all files in the dictionary.

    Args:
        dset_dict: The data dictionary.
        exceptions_list: List of strings of file names that will throw exceptions.
        final_grid: Dataset of the final grid.
        data_path_out: String name of the output path to put the saved files.
    """
    for key in dset_dict.keys():
        # Generate new filename for intermediate processed data
        fname = generate_new_filename(key)

        # Check if one of cases that throws exceptions (to investigate later)
        if fname in exceptions_list:
            print('******** skipping ************')
        else:
            # Process data
            ds_processed = process_dataset(key, dset_dict, final_grid)

            # Save processed data
            save_dataset(ds_processed, fname, data_path_out)
