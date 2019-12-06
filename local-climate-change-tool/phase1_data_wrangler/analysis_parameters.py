"""
Defines parameters for what data to use and where data is saved
"""

######### Settings for data dictionary
EXPERIMENT_LIST = ['historical', 'ssp126', 'ssp370', 'ssp245', 'ssp585']
VARIABLE_ID = 'tas'
TABLE_ID = 'Amon'
GRID_LABEL = 'gn'

######### Data Directory Information
DIR_HOME = '/home/jovyan/local-climate-data-tool/'           #
DIR_UTIL = DIR_HOME + 'local-climate-change-tool/'
DIR_DATA = DIR_HOMEL + 'data/'
DIR_CATALOG = DIR_DATA + 'catalogs/'
DIR_TESTING_DATA = DIR_DATA + 'files_for_testing/'
DIR_DUMMY_DATA = DIR_DATA + 'dummy_data_temporary/'
DIR_DATA_INTERMED = DIR_DATA + 'intermediate_processed_data/'
DIR_INTERMEDIATE_PROCESSED_MODEL_DATA = DIR_DATA_INTERMED + 'Processed_Model_Data/'
DIR_INTERMEDIATE_OBSERVATION_DATA  = DIR_DATA_INTERMED + 'Raw_Historical_Observations/'
DIR_PROCESSED_DATA = DIR_DATA + 'processed_data/'

DIR_GOOGLE_DRIVE_PERMISSIONS = DIR_DATA + 'catalogs/'