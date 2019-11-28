"""
Tests subcomp e
"""
import glob
import xarray as xr
import numpy as np

import analysis_parameters as params
import subcomp_e_compute_global_mean_data as process_global_mean_data

INTERMEDIATE_MODEL_DIR = params.DIR_TESTING_DATA+'processed_model_data'
OUT_DIR = params.DIR_TESTING_DATA
TEST_KEY = 'tas_historical_CAMS-CSM1-0'

PROCESSED_DICT = process_global_mean_data.read_zarr_files(data_path=INTERMEDIATE_MODEL_DIR)
#for key in PROCESSED_DICT.keys():
    # compute the global mean
#    ds_global_mean = compute_global_mean(PROCESSED_DICT, key)

#    # save the global mean dataset
#    save_dataset(ds_global_mean)

def test_read_zarr_files(data_dict=PROCESSED_DICT):
    assert DATA_DICT is not None
    ### TEST THIS###

def test_compute_global_mean(data_dict=PROCESSED_DICT, this_key=TEST_KEY):
    mean_dataset = process_global_mean_data.compute_global_mean(data_dict, this_key)
    
    assert mean_dataset is not None

#def test_save_dataset(ds):