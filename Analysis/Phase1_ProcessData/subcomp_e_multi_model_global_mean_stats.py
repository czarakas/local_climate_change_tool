"""
Module to generate datasets of multimodel statistics for each of the CMIP6
scenarios for the global mean data (dimension time).

Author: Jacqueline Nugent
Last Modified: November 24, 2019
"""
import glob
import xarray as xr
import numpy as np

import analysis_parameters


OUT_DIR = analysis_parameters.DIR_PROCESSED_DATA + 'model_data/global_mean_data/'
SCENARIOS = analysis_parameters.EXPERIMENT_LIST


def read_zarr_files(data_path):
    """
    Open all <fname>.zarr files in the data_path. Returns a dictionary with
    key scenario name and value list of datasets in the scenario.
    """
    # open zarr files & get list of datasets for each scenario
    nexp = len(SCENARIOS)
    ds_list = [[] for i in range(nexp)]
    for s in range(nexp):
        sname = SCENARIOS[s]
        files = [f for f in glob.glob(data_path + '*_' + sname + '_*.zarr')]
        datasets = [xr.open_zarr(f) for f in files]
        ds_list[s] = datasets

    # make the dictionary
    data_dict = dict(zip(SCENARIOS, ds_list))

    return data_dict


def compute_stats(datasets, file_names):
    """
    Compute the mean, minimum, maximum, and standard deviation values of one
    variable across the global means of each model.

    Args:
        datasets, list of the processed global mean Datasets in one scenario
        file_names, list of the names of the zarr files containing the
                    datasets in the form
                    "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"
    Returns:
        stats_list, a list of DataArrays containing the computed statistics
                    in the form [multi_mean, multi_max, multi_min, multi_std].
    """
    times = datasets[0].time
    varname = file_names[0].split("_")[0]
    model_global_means = np.empty((len(datasets), len(times)))

    ### loop through models to select global mean at each time step
    for i in range(len(datasets)):
        model_global_means[i, :] = datasets[i][varname]

    ### calculate statistics
    multi_mean_calc = np.nanmean(model_global_means, axis=0)
    multi_min_calc = np.nanmin(model_global_means, axis=0)
    multi_max_calc = np.nanmax(model_global_means, axis=0)
    multi_std_calc = np.nanstd(model_global_means, axis=0)

    ### create the DataArrays
    multi_mean = xr.DataArray(data=multi_mean_calc, coords={'time': times}, dims='time')
    multi_min = xr.DataArray(data=multi_min_calc, coords={'time': times}, dims='time')
    multi_max = xr.DataArray(data=multi_max_calc, coords={'time': times}, dims='time')
    multi_std = xr.DataArray(data=multi_std_calc, coords={'time': times}, dims='time')

    stats_list = [multi_mean, multi_min, multi_max, multi_std]

    return stats_list


def export_stats(datasets, file_names):
    """
    Exports the computed multimodel statistics to a Dataset.

    as Dataset with dimension time and variables multi_mean, multi_min, multi_max,
    and multi_std. Scenario name and variable name (e.g. 'tas') are attributes
    of the dataset.

    Args:
        datasets, list of the processed global mean Datasets in one scenario
        file_names, list of the names of the zarr files containing the
                    datasets in the form
                    "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"
    Returns:
        multi_stats, a Dataset with dimensions latitude, longitude, and time;
                    variables multi_mean, multi_min, multi_max, and multi_std;
                    and attributes variable (name of the variable, e.g. 'tas')
                    and scenario (name of the scenario, e.g. 'historical').
    Exceptions:
        ValueError, raised if datasets and file_names have different lengths
    """
    ### check that datasets and file_names have the same length
    check = len(datasets) == len(file_names)
    if not check:
        raise ValueError('Length of file_names must be the same as length of'
                         'datasets.')

    ### get the name of the scenario
    this_scenario = file_names[0].split('_')[1]
    this_var = file_names[0].split('_')[0]

    ### calculate statistics
    [mm_mean, mm_min, mm_max, mm_std] = compute_stats(datasets, file_names)

    ### make dictionary for the data
    varnames = ['mean', 'min', 'max', 'stdev']
    stats = [mm_mean, mm_min, mm_max, mm_std]
    stats_dict = dict(zip(varnames, stats))

    ### export it into a single Dataset
    multi_stats = xr.Dataset(data_vars=stats_dict,
                             attrs={'variable': this_var,
                                    'scenario': this_scenario})

    return multi_stats


def save_dataset(ds, out_path):
    """Save the multimodel statistics dataset as a zarr file."""
    ds.load()
    file_name = ds.variable + '_' + ds.scenario + '_GLOBALMEAN_STATS'
    ds.chunk({'time':10})
    ds.to_zarr(out_path + file_name + '.zarr')


##################### Main Workflow ##########################################

def process_all_scenarios(data_path, data_path_out=OUT_DIR):
    """Process all scenarios"""
    # read in the processed model data files
    global_mean_dict = read_zarr_files(data_path)

    for key in global_mean_dictkeys():
        # make a list of the datasets and filenames
        dataset_list = global_mean_dict[key]
        fnames = [dataset.file_name for dataset in dataset_list]

        # generate the multimodel stats dataset
        ds_gm_stats = export_stats(dataset_list, fnames)

        # save the dataset
        save_dataset(ds_gm_stats, data_path_out)