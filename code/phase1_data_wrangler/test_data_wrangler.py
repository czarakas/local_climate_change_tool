import xarray as xr
import data_wrangler as dw
import analysis_parameters as params

# Define directory and file names
DIR_TESTING = params.DIR_DUMMY_DATA
TEST_KEY1 = 'ScenarioMIP.MOHC.UKESM1-0-LL.ssp585.Amon.gn'
TEST_KEY2 = 'CMIP.CAMS.CAMS-CSM1-0.historical.Amon.gn'

TESTING_DATA_DIR = '/home/jovyan/local-climate-data-tool/data/files_for_testing/raw_data/'
TESTING_OUTPUT_DIR = '/home/jovyan/local-climate-data-tool/data/files_for_testing/processed_model_data/'
VARNAME = params.VARIABLE_ID

# Read testing data into dictionary
DSET_DICT = dict()
DSET_DICT[TEST_KEY1] = 57#xr.open_dataset(TESTING_DATA_DIR+TEST_KEY1+'.nc')
DSET_DICT[TEST_KEY2] = 57#xr.open_dataset(TESTING_DATA_DIR+TEST_KEY2+'.nc')

def test_print_time():
    dw.print_time()

def test_subcomp_a(experiment_ID='ssp126'):
    dset_dict = dw.subcomponent_a(print_statements_on=True)

#def test_subcomp_b(ref_grid_key='TEST_KEY2',dset_dict=DSET_DICT,
#                   print_statements_on=True, data_dir=DIR_TESTING+'raw_data/'):
#    dw.subcomponent_b(ref_grid_key, dset_dict, print_statements_on, data_dir)


def main():
    #TO DO: function to call test modules should be added!
    print("it works")


if __name__ == "__main__":
    main()
