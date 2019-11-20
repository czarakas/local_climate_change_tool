"""
Module to generate datasets of global means for each of the processed CMIP6
zarr files.

Running this script for all models take about 5 minutes.

Make sure to clear the directory you would like the zarr files to be saved
in - something about this format makes it not work to overwrite existing
files.

Author: Jacqueline Nugent
Last Modified: November 20, 2019
"""
import glob
import xarray as xr
import numpy as np

import analysis_parameters

INTERMEDIATE_MODEL_DIR = analysis_parameters.DIR_INTERMEDIATE_PROCESSED_MODEL_DATA
INTERMEDIATE_GLOBAL_DIR = analysis_parameters.DIR_INTERMEDIATE_PROCESSED_GLOBAL_DATA
OUT_DIR = INTERMEDIATE_GLOBAL_DIR + 'GlobalMeanData/'


def read_zarr_files(data_path):
    """
    Open all <fname>.zarr files in the data_path. Returns a dictionary with
    key filename and value dataset.
    """
    # open the zarr files
    files = [f for f in glob.glob(data_path + '*.zarr')]
    datasets = [xr.open_zarr(f) for f in files]

    # make the dictionary
    endcut = -1*len('.zarr')
    begcut = len(data_path)
    fnames = [f[begcut:endcut] for f in files]
    data_dict = dict(zip(fnames, datasets))

    return data_dict


def compute_global_mean(data_dict, this_key):
    """
    Compute the global average of model data from this model, for this
    scenario, and for variable varname. Exports the mean as a new
    Dataset with dimension time.

    Pass in key from the data_dict (var_scenario_model).
    """
    ### get information from the data_dict
    model_data = data_dict[this_key]
    varname = this_key.split('_')[0]

    ### average data globally
    ntime = len(model_data.time)
    mean_data = np.empty(ntime)
    mean_data[:] = model_data[varname].mean(dim=['lat', 'lon'], skipna=True)

    ### export as a dataset
    times = model_data.time
    fname = this_key + '_GLOBALMEAN'
    mean_xarray = xr.DataArray(data=mean_data, coords={'time': times}, dims='time')
    mean_dataset = xr.Dataset(data_vars={varname: mean_xarray},
                              coords={'time': times},
                              attrs={'file_name': fname})

    return mean_dataset


def save_dataset(ds):
    """Save the global mean dataset as a zarr file"""
    ds.load()
    ds.chunk({'time':10})
    ds.to_zarr(OUT_DIR + ds.file_name + '.zarr')


######### MAIN WORKFLOW: #########

PROCESSED_DICT = read_zarr_files(INTERMEDIATE_MODEL_DIR)

for key in PROCESSED_DICT.keys():
    # compute the global mean
    ds_global_mean = compute_global_mean(PROCESSED_DICT, key)

    # save the global mean dataset
    save_dataset(ds_global_mean)