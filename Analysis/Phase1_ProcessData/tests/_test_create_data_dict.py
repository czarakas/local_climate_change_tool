"""
Runs test on data dictionary
"""

import xarray as xr
import numpy as np
import AnalysisParameters
import CreateDataDict

######### Read in Settings for Data Dictionary
THIS_EXPERIMENT_ID = AnalysisParameters.EXPERIMENT_LIST
THIS_VARIABLE_ID = AnalysisParameters.VARIABLE_ID
THIS_TABLE_ID = AnalysisParameters.TABLE_ID
THIS_GRID_LABEL = AnalysisParameters.GRID_LABEL
OUTPUT_PATH = AnalysisParameters.DIR_PROCESSED_DATA

######### Create Data Dictionary to test
[DATASET_INFO,
 DSET_DICT,
 MODELNAMES] = CreateDataDict.create_data_dict(THIS_EXPERIMENT_ID,
                                               THIS_VARIABLE_ID,
                                               THIS_TABLE_ID,
                                               THIS_GRID_LABEL)

EXPECTED_COORDS = ['lat', 'lon', 'time', 'member_id']

########## Define test functions

def test_type():
    """Tests that each dataset in the dictionary is an xarray dataset"""
    all_datasets_pass = True
    for key in DSET_DICT.keys():
        ds = DSET_DICT[key]
        if isinstance(ds, xr.core.dataset.Dataset):
            pass
        else:
            all_datasets_pass = False
    assert all_datasets_pass

def test_coords():
    """Tests that each dataset in the dictionary has coordinates of lat/lon/time/member_id
    and no other coordinates"""
    all_datasets_pass = True
    for key in DSET_DICT.keys():
        ds = DSET_DICT[key]
        coordnames = [coord for coord in ds[THIS_VARIABLE_ID].coords]
        if set(coordnames) == set(EXPECTED_COORDS):
            pass
        else:
            all_datasets_pass = False
            print(key)
    assert all_datasets_pass

def test_coords_no_duplicates():
    """Tests that there are no duplicates in any coordinate values"""
    all_datasets_pass = True
    for key in DSET_DICT.keys():
        ds = DSET_DICT[key]
        no_duplicates = True
        for coord in ds[THIS_VARIABLE_ID].coords:
            coord_vals = ds[THIS_VARIABLE_ID][coord].values
            unique_vals, counts = np.unique(coord_vals, return_counts=True)
            duplicates = unique_vals[counts > 1]
            if len(duplicates) == 0:
                no_duplicates_thiscoord = True
            else:
                no_duplicates_thiscoord = False
            no_duplicates = no_duplicates and no_duplicates_thiscoord
        if no_duplicates:
            pass
        else:
            all_datasets_pass = False
            print(key)
    assert all_datasets_pass

#def test_variable_type():
#    """Tests that each dataset in the dictionary has expected type for variable of interest"""
#    all_datasets_pass = True
#    for key in DSET_DICT.keys():
#        ds = DSET_DICT[key]
#        if type(ds[THIS_VARIABLE_ID].values[0, 0, 0, 0]) == np.float32:
#            pass
#        else:
#            all_datasets_pass = False
#            print(key)
#    assert all_datasets_pass

#def test_variable_no_nans():
#    """Tests that each dataset in the dictionary has no NaNs for variable of interest"""
#    all_datasets_pass = True
#    for key in DSET_DICT.keys():
#        ds = DSET_DICT[key]
#        if not np.isnan(ds[THIS_VARIABLE_ID].values).any():
#            pass
#        else:
#            all_datasets_pass = False
#            print(key)
#    assert all_datasets_pass
