"""
test_subcomp_a.py

Contains the test class for subcomp_a_create_data_dict.py.
"""
import unittest
import pandas as pd

from phase1_data_wrangler.subcomp_a_create_data_dict import create_data_dict
from phase1_data_wrangler.analysis_parameters import TABLE_ID, GRID_LABEL

SCENARIO_NAME = 'ssp126'
VARIABLE_NAME = 'tas'

[DATASET_INFO,
 DSET_DICT,
 MODELNAMES] = create_data_dict(this_experiment_id=SCENARIO_NAME,
                                this_variable_id=VARIABLE_NAME,
                                this_table_id=TABLE_ID,
                                this_grid_label=GRID_LABEL)

EXPECTED_COLS = ['activity_id', 'institution_id', 'source_id', 'experiment_id',
                 'member_id', 'table_id', 'variable_id', 'grid_label', 'zstore',
                 'dcpp_init_year']

class TestClassA(unittest.TestCase):
    """Test class for subcomp_a_create_data_dict.py"""

    def test_dset_exists(self, dset_dict=DSET_DICT):
        """Test that the dictionary exists."""
        self.assertTrue(isinstance(DSET_DICT, dict))
        self.assertTrue(dset_dict is not None)

    def test_dset_full(self, dset_dict=DSET_DICT):
        """Test that the dictionary has keys."""
        self.assertTrue(len(dset_dict.keys()) > 0)

    def test_dataset_info(self, dataset_info=DATASET_INFO, expected_cols=EXPECTED_COLS):
        """Test that dataset_info is a nonempty DataFrame with the expected columns."""
        self.assertTrue(isinstance(dataset_info, pd.core.frame.DataFrame))
        self.assertTrue(len(dataset_info) > 0)
        self.assertEqual(set(dataset_info.columns), set(expected_cols))

    def test_modelnames_list(self, modelnames=MODELNAMES):
        """Test that modelnames is a nonempty list of strings."""
        self.assertTrue(len(modelnames) > 0)
        self.assertTrue(isinstance(modelnames, list))
        self.assertTrue(isinstance(modelnames[0], str))


if __name__ == '__main__':
    unittest.main()
