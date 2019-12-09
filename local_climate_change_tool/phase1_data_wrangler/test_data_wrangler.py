"""
Test data_wrangler
"""
import unittest
import os

from phase1_data_wrangler.analysis_parameters import DIR_TESTING_DATA
from phase1_data_wrangler.data_wrangler import print_time, delete_zarr_files

# Define directory and a dummy file to test deletions
DIR_TESTING_FILES = DIR_TESTING_DATA
DUMMY_NAME = 'foo'
DUMMY_EXT = '.txt'
DUMMY_FILE = DUMMY_NAME + DUMMY_EXT

class TestDataWrangler(unittest.TestCase):
    """Unit test for data_wrangler.py"""
    def test_print_time(self):
        """Test that the print_time function executes without exceptions"""
        print_time()
        self.assertTrue(True)

    def test_delete_zarr_files(self):
        """Tests that delete_zarr_files function deletes the expected file"""
        open(DIR_TESTING_FILES + DUMMY_FILE, 'x')
        delete_zarr_files(data_dir=DIR_TESTING_FILES, regex=DUMMY_NAME,
                          file_type=DUMMY_EXT)
        self.assertFalse(os.path.isfile(DIR_TESTING_FILES + DUMMY_FILE))

if __name__ == "__main__":
    unittest.main()
