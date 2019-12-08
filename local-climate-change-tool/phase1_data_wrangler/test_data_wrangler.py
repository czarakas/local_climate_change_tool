import sys
import unittest
import xarray as xr
import data_wrangler as dw
import analysis_parameters as params
import unittest
import pytest
import os
import time

# Define directory and a dummy file to test deletions
DIR_TESTING_FILES = params.DIR_TESTING_DATA
DUMMY_NAME = 'foo'
DUMMY_EXT = '.txt'
DUMMY_FILE = DUMMY_NAME + DUMMY_EXT

class test_data_wrangler(unittest.TestCase):
    def test_print_time(self):
        """Test that the print_time function executes without exceptions"""
        dw.print_time()
        self.assertTrue(True)

    def test_delete_zarr_files(self):
        """Tests that delete_zarr_files function deletes the expected file"""
        open(DIR_TESTING_FILES + DUMMY_FILE, 'x')
        dw.delete_zarr_files(data_dir = DIR_TESTING_FILES, regex=DUMMY_NAME,
                       file_type=DUMMY_EXT)
        self.assertFalse(os.path.isfile(DIR_TESTING_FILES + DUMMY_FILE))
    
    def test_subcomps(self):
        """Runs tests for each of the subcomponents."""
        pytest.main(["test_subcomp_a.py"])
        pytest.main(["test_subcomp_b.py"])
        pytest.main(["test_subcomp_c.py"])
#         pytest.main(["test_subcomp_d.py"])
    

if __name__ == "__main__":
    unittest.main()
