"""
analysis_parameters.py

Defines parameters for what data to use and where data is saved.
"""
import os

######### Settings for Data Dictionary
EXPERIMENT_LIST = ['historical', 'ssp126', 'ssp370', 'ssp245', 'ssp585']
VARIABLE_ID = 'tas'
TABLE_ID = 'Amon'
GRID_LABEL = 'gn'

######### Gets Home Directory
CWD = os.getcwd()
PROJECT_FOLDER_NAME = '/local_climate_change_tool/'
PROJECT_FOLDER_LOCATION = CWD.split(PROJECT_FOLDER_NAME, 1)[0]

DIR_HOME = PROJECT_FOLDER_LOCATION + PROJECT_FOLDER_NAME
if '/local_climate_change_tool/local_climate_change_tool' in DIR_HOME:
    DIR_HOME = PROJECT_FOLDER_LOCATION + '/'

######### Data Directory Information
DIR_UTIL = DIR_HOME + 'local_climate_change_tool/'
DIR_DATA = DIR_HOME + 'data/'
DIR_CATALOG = DIR_DATA + 'catalogs/'
DIR_TESTING_DATA = DIR_DATA + 'files_for_testing/'
DIR_DUMMY_DATA = DIR_DATA + 'dummy_data_temporary/'
DIR_DATA_INTERMED = DIR_DATA + 'intermediate_processed_data/'
DIR_INTERMEDIATE_PROCESSED_MODEL_DATA = DIR_DATA_INTERMED + 'Processed_Model_Data/'
DIR_INTERMEDIATE_OBSERVATION_DATA = DIR_DATA_INTERMED + 'Raw_Historical_Observations/'
DIR_PROCESSED_DATA = DIR_DATA + 'processed_data/'

DIR_GOOGLE_DRIVE_PERMISSIONS = DIR_DATA + 'catalogs/'
