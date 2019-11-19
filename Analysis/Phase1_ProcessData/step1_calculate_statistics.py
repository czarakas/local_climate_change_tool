"""
This module generates datasets of multimodel statistics for each of the CMIP6
scenarios for the global mean data (dimension time).

Modified from step1_process_climate_model_data.py and
step1_compute_global_mean_data.py.

Make sure to clear the directory you would like the zarr files to be saved in - something about
this format makes it not work to overwrite existing files.

Author: Jacqueline Nugent
Last Modified: November 19, 2019
"""
import xarray as xr
import glob
import numpy as np

import analysis_parameters
import multimodelstats as mms


INTERMEDIATE_DIR = analysis_parameters.DIR_INTERMEDIATE_DATA
GLOBAL_DIR = INTERMEDIATE_DIR + 'GlobalMeanData/'
OUT_DIR = INTERMEDIATE_DIR + '../MultimodelStatistics/'
SCENARIOS = analysis_parameters.EXPERIMENT_LIST

def read_zarr_files(data_path):
    """
    Open all <fname>.zarr files in the data_path. Returns a dictionary with
    key scenario name and value list of datasets in the scenario.
    """
    # open zarr files & get list of datasets for each scenario
    nexp = len(SCENARIOS)
    ds_list = [[] for i in range(nexp)]
    for s in range(nexp):
        sname = SCENARIOS[s]
        files = [f for f in glob.glob(data_path + '*_' + sname + '_*.zarr')]
        datasets = [xr.open_zarr(f) for f in files]
        ds_list[s] = datasets

    # make the dictionary
    data_dict = dict(zip(SCENARIOS, ds_list))

    return data_dict


def save_dataset(ds, out_path):
    """Save the multimodel statistics dataset as a zarr file"""
    ds.load()
    file_name = ds.variable + '_' + ds.scenario + '_GLOBALMEAN_STATS'
    ds.chunk({'time':10})
    ds.to_zarr(out_path + file_name + '.zarr')

    
####### MAIN WORKFLOW ########

GLOBAL_MEAN_DICT = read_zarr_files(GLOBAL_DIR)

### for global mean files:
for key in GLOBAL_MEAN_DICT.keys():
    # compute the global mean multimodel stats
    ds_list = GLOBAL_MEAN_DICT[key]
    fnames = [ds.file_name for ds in ds_list]
    ds_gm_stats = mms.export_stats(ds_list, fnames)
    
    # save the global mean multitmodel stats dataset
    save_dataset(ds_gm_stats, OUT_DIR)
    