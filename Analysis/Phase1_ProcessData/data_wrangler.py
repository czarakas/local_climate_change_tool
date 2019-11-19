"""
Complete Module 1: Data Wrangler
"""

import os
import glob
import analysis_parameters
import subcomp_a_create_data_dict as data_dict
import subcomp_a_process_climate_model_data as process_data
import subcomp_b_multi_model_stats as generate_stats

#----------------------------------------------------------------------
# GLOBAL PARAMETER SETTINGS
#----------------------------------------------------------------------
PRINT_STATEMENTS_ON = True
SCENARIO_LIST = analysis_parameters.EXPERIMENT_LIST
VARIABLE_NAME = analysis_parameters.VARIABLE_ID
TABLE_ID = analysis_parameters.TABLE_ID
GRID_LABEL = analysis_parameters.GRID_LABEL
OUTPUT_PATH = analysis_parameters.DIR_PROCESSED_DATA
CURRENT_PATH = '/home/jovyan/local-climate-data-tool/Analysis/Phase1_ProcessData/'
DIR_INTERMEDIATE = analysis_parameters.DIR_INTERMEDIATE_PROCESSED_MODEL_DATA

EXCEPTIONS_LIST = ('tas_historical_CESM2',
                   'tas_ssp126_CanESM5', 'tas_ssp126_CAMS-CSM1-0',
                   'tas_ssp245_CAMS-CSM1-0', 'tas_ssp245_HadGEM3-GC31-LL',
                   'tas_ssp370_CESM2-WACCM', 'tas_ssp370_MPI-ESM1-2-HR',
                   'tas_ssp370_CAMS-CSM1-0', 'tas_ssp370_BCC-ESM1',
                   'tas_ssp585_CAMS-CSM1-0', 'tas_ssp585_CanESM5'
                  )

REFERENCE_GRID_KEY = 'CMIP.BCC.BCC-CSM2-MR.historical.Amon.gn'

#----------------------------------------------------------------------
# FUNCTION DEFINITIONS
#----------------------------------------------------------------------

def delete_zarr_files(data_dir, regex):
    """Deletes zarr files matching regular expression. This is a
    necessary function because zarr files cannot be overwritten"""
    i = 0
    for file in glob.glob(data_dir+regex+'.zarr'):
        os.system('rm -rf '+file)
        i = i+1
    print('deleted '+str(i)+' files in '+data_dir)

def subcomponent_a(ref_grid_key, print_statements_on=False):
    """Subcomponent a"""
    # Delete existing files because you can't overwrite zarr files
    if print_statements_on:
        print('---> Deleting existing intermediate model data files')
    delete_zarr_files(data_dir='/home/jovyan/local-climate-data-tool/Data/'+
                      'IntermediateData/Processed_Model_Data/',
                      regex=VARIABLE_NAME+'_*')

    if print_statements_on:
        print('---> Creating data dictionary of available model data')
    [_, dset_dict, _] = data_dict.create_data_dict(this_experiment_id=SCENARIO_LIST,
                                                   this_variable_id=VARIABLE_NAME,
                                                   this_table_id=TABLE_ID,
                                                   this_grid_label=GRID_LABEL)

    if print_statements_on:
        print('---> Creating reference grid for data regridding')
    final_grid = process_data.create_reference_grid(reference_key=ref_grid_key,
                                                    dset_dict=dset_dict)

    if print_statements_on:
        print('---> Generating consistent data files for each model and scenario')
    process_data.process_all_files_in_dictionary(dset_dict=dset_dict,
                                                 exceptions_list=EXCEPTIONS_LIST,
                                                 final_grid=final_grid)

def subcomponent_b(num_chunks, normalized, print_statements_on=False):
    """Subcomponent b"""
    # Delete existing files because you can't overwrite zarr files
    if print_statements_on:
        print('---> Deleting existing processed data files')
    delete_zarr_files(data_dir='/home/jovyan/local-climate-data-tool/Data/ProcessedData/',
                      regex='modelData_'+VARIABLE_NAME+'_*')

    if print_statements_on:
        print('---> Generating multimodel statistics')
    generate_stats.process_all_scenarios(data_path=DIR_INTERMEDIATE,
                                         variable_name=VARIABLE_NAME,
                                         scenario_list=SCENARIO_LIST,
                                         num_chunks=num_chunks,
                                         normalized=normalized)

def main(print_statements_on=PRINT_STATEMENTS_ON):
    """Main module runs both subcomponent a and b"""
    if print_statements_on:
        print('---------------Running subcomponent A---------------')
    subcomponent_a(ref_grid_key=REFERENCE_GRID_KEY,
                   print_statements_on=print_statements_on)
    
    if print_statements_on:
        print('---> Deleting regridding intermediate files')
    delete_zarr_files(data_dir=CURRENT_PATH,
                      regex='nearest_s2d_*')
    
    
    if print_statements_on:
        print('---------------Running subcomponent B---------------')
    subcomponent_b(num_chunks=20, normalized=False, print_statements_on=print_statements_on)

if __name__ == '__main__':
    main()
