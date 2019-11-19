"""
Add docstring
"""

import time
import analysis_parameters
import subcomp_b_multi_model_stats as scb

DATA_PATH = analysis_parameters.DIR_INTERMEDIATE_DATA+'Processed_Model_Data/'
SCENARIO_LIST = analysis_parameters.EXPERIMENT_LIST

def normalize_ds(data_path, fname):
    """Add docstring"""
    ds = scb.read_in_fname(data_path=data_path, fname=fname)
     #--------------- Calculate baseline ---------------
    variable_name = fname.split("_")[0]
    model_name = fname.split("_")[2]
    fname_hist = variable_name+'_'+'historical'+'_'+model_name
    print(fname_hist)

    if model_name in ('MPI-ESM1-2-HR', 'CESM2'):
        print(' skipping' + model_name)
        ds_norm = None
    else:
        ds_hist = scb.read_in_fname(data_path=data_path, fname=fname_hist)
        ds_hist_subset = ds_hist.sel(time=slice('1850-01', '1950-12'))
        ds_hist_baseline = ds_hist_subset.mean(dim='time').load()
        ds_norm = ds - ds_hist_baseline
    return ds_norm

def save_dataset(data_path, ds, this_fname):
    """Saves processed dataset as zarr file"""
    ds.load()
    # Export intermediate processed dataset as zarr file
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(data_path+this_fname+'.zarr')

def normalize_scenario_files(scenario, data_path=DATA_PATH):
    """Add docstring"""
    filenames = scb.get_scenario_fnames(data_path, scenario)
    nmodels = len(filenames)

    for i in range(0, nmodels):
        fname = filenames[i]
        ds_norm = normalize_ds(data_path=data_path, fname=fname)

        if ds_norm is not None:
            fname_new = 'Normalized_'+fname
            save_dataset(data_path, ds_norm, fname_new)


#------------------MAIN WORKFLOW----------------------------------------
for scenario in SCENARIO_LIST:
    start_time = time.time()
    print('----------'+scenario+'----------')
    normalize_scenario_files(scenario)
    end_time = time.time()
    print(end_time - start_time)
