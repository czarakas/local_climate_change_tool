"""
Module to compute multimodel statistics (ignoring NaN values) for the global
mean files and generate an xarray containing the statistics as variables.

Functions:
    multi_model_mean, compute multimodel mean
    multi_model_min, compute multimodel minimum
    multi_model_max, compute multimodel maximum
    multi_model_stdev, compute multimodel standard deviation
    export_stats, export dataset statistics into single Dataset

Author: Jacqueline Nugent
Last Modified: November 19, 2019
"""
import warnings
import xarray as xr
import numpy as np


def multi_model_mean(datasets, file_names):
    """
    Compute the mean value of one variable, averaged over the globe, across
    the given models for one scenario.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"

    Returns:
        multi_mean (DataArray), array of multi-model mean of this variable for
                        this scenario with dimension time
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0 
    model_means = np.empty((nmodels, ntime))

    ### loop through models
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # select global mean at each time step:
        model_means[i, :] = model[varname]

    multi_mean_calc = np.nanmean(model_means, axis=0)
    
    ### create the DataArray
    multi_mean = xr.DataArray(data=multi_mean_calc, coords={'time': times}, dims='time')
    
    return multi_mean


def multi_model_min(datasets, file_names):
    """
    Compute the minimum value of one variable, averaged over the globe, across
    the given models for one scenario.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"

    Returns:
        multi_min (DataArray), array of multi-model minimum of this variable
                        for this scenario with dimension time
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_mins = np.empty((nmodels, ntime))
    
    ### loop through models
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # select global mean at each time step:
        model_mins[i, :] = model[varname]

    ### compute multimodel minimum
    multi_min_calc = np.nanmin(model_mins, axis=0)
    
    ### create the DataArray
    multi_min = xr.DataArray(data=multi_min_calc, coords={'time': times}, dims='time')
    
    return multi_min


def multi_model_max(datasets, file_names):
    """
    Compute the maximum value of one variable, averaged over the globe, of one
    variable across the given models for one scenario.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"

    Returns:
        multi_max (DataArray), array of multi-model maximum of this variable
                        for this scenario with dimension time
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_maxes = np.empty((nmodels, ntime))
    
    ### loop through models
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # select global mean at each time step:
        model_maxes[i, :] = model[varname]

    ### compute multimodel maximum
    multi_max_calc = np.nanmax(model_maxes, axis=0)
    
    ### create the DataArray
    multi_max = xr.DataArray(data=multi_max_calc, coords={'time': times}, dims='time')

    return multi_max


def multi_model_std(datasets, file_names):
    """
    Compute the standard deviation of one variable, averaged over the globe,
    across the given models for one scenario.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"

    Returns:
        multi_std (DataArray), array of multi-model standard deviation of this
                        variable for this scenario with dimension time
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_stdevs = np.empty((nmodels, ntime))

    ### loop through models
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # select global mean at each time step:
        model_stdevs[i, :] = model[varname]

    ### compute multimodel standard deviation
    multi_std_calc = np.nanstd(model_stdevs, axis=0)
    
    ### create the DataArray
    multi_std = xr.DataArray(data=multi_std_calc, coords={'time': times}, dims='time') 
    
    return multi_std


def export_stats(datasets, file_names):
    """
    Main function to run for module. Exports the multimodel statistics as a
    Dataset with dimension time and variables multi_mean, multi_min, multi_max,
    and multi_std. Scenario name and variable name (e.g. 'tas') are attributes
    of the dataset.
    
    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL_GLOBALMEAN.zarr"

    Returns:
        multi_stats (Dataset), the time series of multi-model statistics
                        of this variable for this scenario
                        
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
    mm_mean = multi_model_mean(datasets, file_names)
    mm_min = multi_model_min(datasets, file_names)
    mm_max = multi_model_max(datasets, file_names)
    mm_std = multi_model_std(datasets, file_names)
    
    ### make dictionary for the data
    varnames = ['multi_mean', 'multi_min', 'multi_max', 'multi_std']
    stats = [mm_mean, mm_min, mm_max, mm_std]
    stats_dict = dict(zip(varnames, stats))
    
    ### export it into a single Dataset
    multi_stats = xr.Dataset(data_vars=stats_dict,
                             attrs={'variable': this_var,
                                    'scenario': this_scenario})
    
    return multi_stats
