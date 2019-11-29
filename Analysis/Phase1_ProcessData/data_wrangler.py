"""
This script runs all subcomponents in the appropriate order to generate
climate data for use in the Dashbboard Generator module.

Approximate run time on ocean.pangeo.io:
A - Create data dictionary of available climate model data:         1   min
B - Process climate model data files to be consistently formatted: 13   mins
C - Process historical observations to be consistently formatted:  ?? mins
D - Calculate summary statistics for each scenario:                 7.5 mins

TOTAL: 23.5 mins

"""
### TODO: fix the docstring above with adjusted times
import os
import time
import glob
import analysis_parameters as params
import subcomp_a_create_data_dict as data_dict
import subcomp_b_process_climate_model_data as process_data
import subcomp_c_multi_model_stats as generate_stats
import subcomp_d_process_historical_obs as process_obs

START_TIME = time.time()

#----------------------------------------------------------------------
# GLOBAL PARAMETER SETTINGS
#----------------------------------------------------------------------
# Settings for this script

PRINT_STATEMENTS_ON = True
EXCEPTIONS_LIST = ('tas_historical_CESM2',
                   'tas_ssp126_CanESM5', 'tas_ssp126_CAMS-CSM1-0',
                   'tas_ssp245_CAMS-CSM1-0', 'tas_ssp245_HadGEM3-GC31-LL',
                   'tas_ssp370_CESM2-WACCM', 'tas_ssp370_MPI-ESM1-2-HR',
                   'tas_ssp370_CAMS-CSM1-0', 'tas_ssp370_BCC-ESM1',
                   'tas_ssp585_CAMS-CSM1-0', 'tas_ssp585_CanESM5'
                  )
REFERENCE_GRID_KEY = 'CMIP.BCC.BCC-CSM2-MR.historical.Amon.gn'

# Parameter names
SCENARIO_LIST = params.EXPERIMENT_LIST
VARIABLE_NAME = params.VARIABLE_ID
TABLE_ID = params.TABLE_ID
GRID_LABEL = params.GRID_LABEL

# Directory information
OUTPUT_PATH = params.DIR_PROCESSED_DATA
CURRENT_PATH = '/home/jovyan/local-climate-data-tool/Analysis/Phase1_ProcessData/'
DIR_INTERMEDIATE = params.DIR_INTERMEDIATE_PROCESSED_MODEL_DATA
DIR_PROCESSED_MODEL_DATA = '/home/jovyan/local-climate-data-tool/data/processed_data/model_data/'
DIR_PROCESSED_OBS_DATA = '/home/jovyan/local-climate-data-tool/data/processed_data/observation_data/'
DIR_INTERMEDIATE_MODEL_DATA = params.DIR_INTERMEDIATE_PROCESSED_MODEL_DATA
DIR_INTER_GLOBAL_DATA = params.DIR_INTERMEDIATE_PROCESSED_GLOBAL_DATA
DIR_PROCESSED_MODEL_DATA_GLOBAL_MEAN = DIR_PROCESSED_MODEL_DATA+'global_mean_data/'
DIR_INTER_OBS_DATA = params.DIR_INTERMEDIATE_OBSERVATION_DATA

#----------------------------------------------------------------------
# FUNCTION DEFINITIONS
#----------------------------------------------------------------------

def print_time(start_time=START_TIME):
    """Prints the minutes elapsed since the start of running the script"""
    current_time = time.time()
    time_elapsed = current_time-start_time
    mins_elapsed = round(time_elapsed/60, 2)
    print('            Time elapsed: '+str(mins_elapsed)+' mins')

def delete_zarr_files(data_dir, regex, print_statements_on=False, file_type='.zarr'):
    """Deletes files matching regular expression. This is a
    necessary function because zarr files cannot be overwritten"""
    i = 0
    for file in glob.glob(data_dir+regex+file_type):
        os.system('rm -rf '+file)
        i = i+1
    if print_statements_on:
        print('   Deleted '+str(i)+' files in '+data_dir)

def subcomponent_a(print_statements_on=False):
    """Creates data dictionary of all available climate model data"""

    if print_statements_on:
        print('====> Creating data dictionary of available model data')
    [_, dset_dict, _] = data_dict.create_data_dict(this_experiment_id=SCENARIO_LIST,
                                                   this_variable_id=VARIABLE_NAME,
                                                   this_table_id=TABLE_ID,
                                                   this_grid_label=GRID_LABEL)
    if print_statements_on:
        print_time()
    return dset_dict

def subcomponent_b(ref_grid_key, dset_dict, print_statements_on=False):
    """Processes raw climate model data to create intermediate spatial model
    files with consistent formatting (dims: lat/lon/time). If intermediate spatial
    model files exist in the output folder when this is run, those existing files
    are deleted"""

    # Delete existing files because you can't overwrite zarr files
    if print_statements_on:
        print('====> Deleting existing intermediate model data files')
    delete_zarr_files(data_dir=DIR_INTERMEDIATE_MODEL_DATA,
                      regex=VARIABLE_NAME+'_*')
    if print_statements_on:
        print_time()

    if print_statements_on:
        print('====> Creating reference grid for data regridding')
    final_grid = process_data.create_reference_grid(reference_key=ref_grid_key,
                                                    dset_dict=dset_dict)
    if print_statements_on:
        print_time()

    if print_statements_on:
        print('====> Generating consistent data files for each model and scenario')
    process_data.process_all_files_in_dictionary(dset_dict=dset_dict,
                                                 exceptions_list=EXCEPTIONS_LIST,
                                                 final_grid=final_grid)
    if print_statements_on:
        print_time()

    if print_statements_on:
        print('====> Deleting regridding intermediate files')
    delete_zarr_files(data_dir=CURRENT_PATH,
                      regex='nearest_s2d_*', file_type='.nc')
    if print_statements_on:
        print_time()

def subcomponent_c(num_chunks, normalized, print_statements_on=False):
    """Processes intermediate spatial model files (dims: lat/lon/time)
    output from subcomponent b to create multimodel statistics (i.e. compressing
    data across all models) of dims: lat/lon/time. If files exist in the output
    folder when this is run, those existing files are deleted"""
    # Delete existing files because you can't overwrite zarr files
    if print_statements_on:
        print('====> Deleting existing processed data files')

    delete_zarr_files(data_dir=DIR_PROCESSED_MODEL_DATA,
                      regex='modelData_'+VARIABLE_NAME+'_*')

    if print_statements_on:
        print_time()

    if print_statements_on:
        print('====> Generating multimodel statistics')
    generate_stats.process_all_scenarios(data_path=DIR_INTERMEDIATE,
                                         variable_name=VARIABLE_NAME,
                                         scenario_list=SCENARIO_LIST,
                                         num_chunks=num_chunks,
                                         normalized=normalized)
    if print_statements_on:
        print_time()

def subcomponent_d(print_statements_on=False):
    """Processes raw historical climate observations to create processed files
    with formatting to match climate model data (dims: lat/lon/time) and
    processed global mean observation files (dims: time). If processed
    historical observation files exist in the output folder when this is run,
    those existing files are deleted"""

    # Delete existing files because you can't overwrite zarr files
    if print_statements_on:
        print('====> Deleting existing processed observation files')
    delete_zarr_files(data_dir=DIR_PROCESSED_OBS_DATA,
                      regex='historical_obs*')
    if print_statements_on:
        print_time()

    if print_statements_on:
        print('====> Processing historical observations')
    process_obs.process_all_observations(data_path=DIR_INTER_OBS_DATA)

    if print_statements_on:
        print_time()

def main(print_statements_on=PRINT_STATEMENTS_ON):
    """ Runs all subcomponents in the appropriate sequence to create
    climate data processed for use in the Dashboard Generator"""

    if print_statements_on:
        print('---------------Running subcomponent A---------------')
    data_dict = subcomponent_a(print_statements_on=print_statements_on)

    if print_statements_on:
        print('---------------Running subcomponent B---------------')
    subcomponent_b(ref_grid_key=REFERENCE_GRID_KEY,
                   dset_dict=data_dict,
                   print_statements_on=print_statements_on)

    if print_statements_on:
        print('---------------Running subcomponent C---------------')
    subcomponent_c(num_chunks=20, normalized=False, print_statements_on=print_statements_on)

    if print_statements_on:
        print('---------------Running subcomponent D---------------')
    subcomponent_d(print_statements_on=print_statements_on)


if __name__ == '__main__':
    main()
