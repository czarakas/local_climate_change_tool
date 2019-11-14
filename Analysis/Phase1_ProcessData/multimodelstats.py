"""
Module to compute multimodel statistics (ignoring NaN values) and generate an
xarray containing the statistics as variables.

This version selects a location first (tested) or takes the global mean (not yet 
tested!) before computing multimodel stats... it took WAY too much memory to
do multimodel mean of all individual points and kept crashing kernel after 4...

*** STILL IN PROGRESS: see TODOs below *** 

Functions:
    multi_model_mean, compute multimodel mean
    multi_model_min, compute multimodel minimum
    multi_model_max, compute multimodel maximum
    multi_model_stdev, compute multimodel standard deviation
    export_stats, export dataset statistics into single Dataset

Author: Jacqueline Nugent
Last Modified: November 14, 2019
"""

### TODO: fix check for consistent times! The first time is bad for one of the 
### global models, so that won't work... have to do something different
### TODO: drop print statements after testing is complete?

import warnings
import xarray as xr
import numpy as np


def multi_model_mean(datasets, file_names, is_global_mean=False, coords=None):
    """
    Compute the mean value of one variable, averaged over the globe or
    at each point, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL.zarr"
        is_global_mean (Boolean), True to return the global multimodel mean;
                        False (Default) to compute the multimodel mean at each
                        lat-lon point
        coords (list of floats), the coordinates in the order [lat, lon] for
                        the location to select if not computing the multimodel
                        global mean; must have length 2

    Returns:
        multi_mean (DataArray), array of multi-model mean of this variable for
                        this scenario with dimension time

    Warnings:
        Warns user if data for a model will be left out of the calculation
        because it does not have the correct number of time steps for this
        scenario (compared to the first model).
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0 
    model_means = np.empty((nmodels, ntime))

    ### loop through models and either calculate global mean or select coords
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # check that it has the same number of time steps as other models
        # in this scenario; skip model if not and warn the user
        if len(model.time) != ntime:
            warnings.warn(('Skipping model {name}: inconsistent number of' +
                           ' time steps for this ' +
                           'scenario').format(name=model_name))
            model_means[i, :] = np.nan
            nskip += 1
            continue
        
        # select global mean at each time step:
        if is_global_mean:
            print('Selecting global mean of {var} for {name}...'.format(
                var=varname, name=model_name))
            model_means[i, :] = model[varname]
        
        # select lat/lon point at each time step:
        else:
            city_lat = coords[0]
            city_lon = coords[1]
            print('Selecting {var} for {name} at ({lat}, {lon})...'.format(
                var=varname, name=model_name, lat=city_lat, lon=city_lon))
            model_means[i, :] = model[varname].sel(lat=city_lat, lon=city_lon,
                                          method='nearest')

    ### compute multimodel mean
    print('Computing multimodel mean of {var} for {num} models...'.format(
        var=varname, num=nmodels-nskip))
    multi_mean_calc = np.nanmean(model_means, axis=0)
    
    ### create the DataArray
    multi_mean = xr.DataArray(data=multi_mean_calc, coords={'time': times}, dims='time')
    
    print(('Returned multimodel man. {num} models skipped.'
           '\n').format(num=nskip))
    
    return multi_mean


def multi_model_min(datasets, file_names, is_global_mean=False, coords=None):
    """
    Compute the minimum value of one variable, averaged over the globe or
    at each point, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL.zarr"
        is_global_mean (Boolean), True to return the global multimodel minimum;
                        False (Default) to compute the multimodel minimum at
                        each lat-lon point
        coords (list of floats), the coordinates in the order [lat, lon] for
                        the location to select if not computing the multimodel
                        global mean; must have length 2

    Returns:
        multi_min (DataArray), array of multi-model minimum of this variable
                        for this scenario with dimension time

    Warnings:
        Warns user if data for a model will be left out of the calculation
        because it does not have the correct number of time steps for this
        scenario (compared to the first model).
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_mins = np.empty((nmodels, ntime))
    
    ### loop through models and either calculate global mean or select coords
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # check that it has the same number of time steps as other models
        # in this scenario; skip model if not and warn the user
        if len(model.time) != ntime:
            warnings.warn(('Skipping model {name}: inconsistent number of' +
                           ' time steps for this ' +
                           'scenario').format(name=model_name))
            model_mins[i, :] = np.nan
            nskip += 1
            continue
        
        # select global mean at each time step:
        if is_global_mean:
            print('Selecting global mean of {var} for {name}...'.format(
                var=varname, name=model_name))
            model_mins[i, :] = model[varname]
        
        # select lat/lon point at each time step:
        else:
            city_lat = coords[0]
            city_lon = coords[1]
            print('Selecting {var} for {name} at ({lat}, {lon})...'.format(
                var=varname, name=model_name, lat=city_lat, lon=city_lon))
            model_mins[i, :] = model[varname].sel(lat=city_lat, lon=city_lon,
                                          method='nearest')

    ### compute multimodel minimum
    print('Computing multimodel minimum of {var} for {num} models...'.format(
        var=varname, num=nmodels-nskip))
    multi_min_calc = np.nanmin(model_mins, axis=0)
    
    ### create the DataArray
    multi_min = xr.DataArray(data=multi_min_calc, coords={'time': times}, dims='time')

    print(('Returned multimodel minimum. {num} models skipped.'
           '\n').format(num=nskip))
    
    return multi_min


def multi_model_max(datasets, file_names, is_global_mean=False, coords=None):
    """
    Compute the maximum value of one variable, averaged over the globe or
    at each point, of one variable across the given models for one
    scenario. Prints to the user what is being done.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL.zarr"
        is_global_mean (Boolean), True to return the global multimodel maximum;
                        False (Default) to compute the multimodel maximum at
                        each lat-lon point
        coords (list of floats), the coordinates in the order [lat, lon] for
                        the location to select if not computing the multimodel
                        global mean; must have length 2

    Returns:
        multi_max (DataArray), array of multi-model maximum of this variable
                        for this scenario with dimension time
                        
    Warnings:
        Warns user if data for a model will be left out of the calculation
        because it does not have the correct number of time steps for this
        scenario (compared to the first model).
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_maxes = np.empty((nmodels, ntime))
    
    ### loop through models and either calculate global mean or select coords
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # check that it has the same number of time steps as other models
        # in this scenario; skip model if not and warn the user
        if len(model.time) != ntime:
            warnings.warn(('Skipping model {name}: inconsistent number of' +
                           ' time steps for this ' +
                           'scenario').format(name=model_name))
            model_maxes[i, :] = np.nan
            nskip += 1
            continue
        
        # select global mean at each time step:
        if is_global_mean:
            print('Selecting global mean of {var} for {name}...'.format(
                var=varname, name=model_name))
            model_maxes[i, :] = model[varname]
        
        # select lat/lon point at each time step:
        else:
            city_lat = coords[0]
            city_lon = coords[1]
            print('Selecting {var} for {name} at ({lat}, {lon})...'.format(
                var=varname, name=model_name, lat=city_lat, lon=city_lon))
            model_maxes[i, :] = model[varname].sel(lat=city_lat, lon=city_lon,
                                          method='nearest')

    ### compute multimodel maximum
    print('Computing multimodel maximum of {var} for {num} models...'.format(
        var=varname, num=nmodels-nskip))
    multi_max_calc = np.nanmax(model_maxes, axis=0)
    
    ### create the DataArray
    multi_max = xr.DataArray(data=multi_max_calc, coords={'time': times}, dims='time')
    
    print(('Returned multimodel maximum. {num} models skipped.'
           '\n').format(num=nskip))    
    
    return multi_max


def multi_model_std(datasets, file_names, is_global_mean=False, coords=None):
    """
    Compute the standard deviation of one variable, averaged over the globe or
    at each point, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL.zarr"
        is_global_mean (Boolean), True to return the global multimodel standard
                        deviation; False (Default) to compute the multimodel
                        standard deviation at each lat-lon point
        coords (list of floats), the coordinates in the order [lat, lon] for
                        the location to select if not computing the multimodel
                        global mean; must have length 2

    Returns:
        multi_std (DataArray), array of multi-model standard deviation of this
                        variable for this scenario with dimension time

    Warnings:
        Warns user if data for a model will be left out of the calculation
        because it does not have the correct number of time steps for this
        scenario (compared to the first model).
    """
    nmodels = len(datasets)
    times = datasets[0].time
    ntime = len(times)
    varname = file_names[0].split("_")[0]
    nskip = 0
    model_stdevs = np.empty((nmodels, ntime))

    ### loop through models and either calculate global mean or select coords
    for i in range(nmodels):
        model = datasets[i]
        model_name = file_names[i].split("_")[2]
        
        # check that it has the same number of time steps as other models
        # in this scenario; skip model if not and warn the user
        if len(model.time) != ntime:
            warnings.warn(('Skipping model {name}: inconsistent number of' +
                           ' time steps for this ' +
                           'scenario').format(name=model_name))
            model_stdevs[i, :] = np.nan
            nskip += 1
            continue
        
        # select global mean at each time step:
        if is_global_mean:
            print('Selecting global mean of {var} for {name}...'.format(
                var=varname, name=model_name))
            model_stdevs[i, :] = model[varname]
        
        # select lat/lon point at each time step:
        else:
            city_lat = coords[0]
            city_lon = coords[1]
            print('Selecting {var} for {name} at ({lat}, {lon})...'.format(
                var=varname, name=model_name, lat=city_lat, lon=city_lon))
            model_stdevs[i, :] = model[varname].sel(lat=city_lat, lon=city_lon,
                                          method='nearest')

    ### compute multimodel standard deviation
    print(('Computing multimodel standard deviation of {var} for {num}' +
          ' models...').format(var=varname, num=nmodels-nskip))
    multi_std_calc = np.nanstd(model_stdevs, axis=0)
    
    ### create the DataArray
    multi_std = xr.DataArray(data=multi_std_calc, coords={'time': times}, dims='time')
    
    print(('Returned multimodel standard deviation. {num} models skipped.'
           '\n').format(num=nskip)) 
    
    return multi_std


def export_stats(datasets, file_names, is_global_mean=False, coords=None):
    """
    Main function to run for module. Exports the multimodel statistics as a
    Dataset with dimension time and variables multi_mean, multi_min, multi_max,
    and multi_std. Scenario name is an attribute of the dataset.
    
    Args:
        datasets (list of Datasets), the preprocessed CMIP6 model data with
                        separate Datasets for each model in this scenario for
                        this variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        file_names (list of strings), list of the names of the zarr files
                        containing the Datasets in the form
                        "VARIABLE_SCENARIO_MODEL.zarr"
        is_global_mean (Boolean), True to return the global multimodel standard
                        deviation; False (Default) to compute the multimodel
                        standard deviation at each lat-lon point
        coords (list of floats), the coordinates in the order [lat, lon] for
                        the location to select if not computing the multimodel
                        global mean; must have length 2

    Returns:
        multi_stats (Dataset), the time series of multi-model statistics
                        of this variable for this scenario

    Exceptions:
        Raises exceptions if is_global_mean=False and coords=None,
        or is_global_mean=False and coords does not have length 2
        
    Warnings:
        Warns user if argument coords is provided when is_global_mean=True
    """
    ### check that arguments for is_global_mean and coords are compatible
    if is_global_mean and coords is not None:
        warnings.warn('Argument coords will be ignored for global mean.')
    if not is_global_mean:
        if coords is None:
            raise Exception('Missing argument coords for a single location.')
        elif len(coords) != 2:
            raise Exception('Must enter coords in the form '
                            '[latitude, longitude].')
    
    ### get the name of the scenario
    this_scenario = file_names[0].split('_')[1]
    
    ### calculate statistics
    mm_mean = multi_model_mean(datasets, file_names, is_global_mean, coords)
    mm_min = multi_model_min(datasets, file_names, is_global_mean, coords)
    mm_max = multi_model_max(datasets, file_names, is_global_mean, coords)
    mm_std = multi_model_std(datasets, file_names, is_global_mean, coords)
    
    ### make dictionary for the data
    varnames = ['multi_mean', 'multi_min', 'multi_max', 'multi_std']
    stats = [mm_mean, mm_min, mm_max, mm_std]
    stats_dict = dict(zip(varnames, stats))
    
    ### export it into a single Dataset
    multi_stats = xr.Dataset(data_vars=stats_dict,
                             attrs={'scenario': this_scenario})
    
    return multi_stats
