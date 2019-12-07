import sys
import unittest
import pandas as pd
import sys
sys.path.append(".")
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

EXPECTED_COLS = ['activity_id', 'institution_id', 'source_id', 'experiment_id',
           'member_id', 'table_id', 'variable_id', 'grid_label', 'zstore',
           'dcpp_init_year']

class test_subcomp_a(unittest.TestCase):
    def test_dset_exists(self, dset_dict=DSET_DICT):
        self.assertTrue(isinstance(DSET_DICT,dict))
        self.assertTrue(dset_dict is not None)

    def test_dset_full(self, dset_dict=DSET_DICT):
        self.assertTrue(len(DSET_DICT.keys()) > 0)

    def test_dataset_info(self, dataset_info=DATASET_INFO, expected_cols=EXPECTED_COLS):
        self.assertTrue(isinstance(dataset_info, pd.core.frame.DataFrame))
        self.assertTrue(len(dataset_info) > 0)
        self.assertEqual(set(dataset_info.columns), set(expected_cols))

    def test_modelnames_list(self, modelnames=MODELNAMES):
        self.assertTrue(len(modelnames) > 0)
        self.assertTrue(isinstance(modelnames,list))
        self.assertTrue(isinstance(modelnames[0],str))

if __name__ == '__main__':
    unittest.main()
