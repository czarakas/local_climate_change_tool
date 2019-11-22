import sys
import pandas as pd

import subcomp_a_create_data_dict as create_data_dict
import analysis_parameters as params

SCENARIO_NAME = 'ssp126'
VARIABLE_NAME = 'tas'
TABLE_ID = params.TABLE_ID
GRID_LABEL = params.GRID_LABEL

[DATASET_INFO,
 DSET_DICT,
 MODELNAMES] = create_data_dict.create_data_dict(this_experiment_id=SCENARIO_NAME,
                                                 this_variable_id=VARIABLE_NAME,
                                                 this_table_id=TABLE_ID,
                                                 this_grid_label=GRID_LABEL)

def test_dset_exists(dset_dict=DSET_DICT):
    assert isinstance(DSET_DICT,dict)
    assert dset_dict is not None

def test_dset_full(dset_dict=DSET_DICT):
    assert len(DSET_DICT.keys()) > 0

EXPECTED_COLS = ['activity_id', 'institution_id', 'source_id', 'experiment_id',
       'member_id', 'table_id', 'variable_id', 'grid_label', 'zstore',
       'dcpp_init_year']

def test_dataset_info(dataset_info=DATASET_INFO, expected_cols=EXPECTED_COLS):
    assert isinstance(dataset_info, pd.core.frame.DataFrame)
    assert len(dataset_info) > 0
    assert set(dataset_info.columns)==set(expected_cols)

def test_modelnames_list(modelnames=MODELNAMES):
    assert len(modelnames) > 0
    assert isinstance(modelnames,list)
    assert isinstance(modelnames[0],str)
    