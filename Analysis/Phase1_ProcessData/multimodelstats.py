"""
Module to compute multimodel statistics. Assumes all models have the same
time coordinates (length and value).

***CURRENTLY UNDERGOING TESTING***

Functions:
    area_mean, average model data over some location
    to_xarray, export the returned numpy arrays of stats to an xarray
    mm_mean, compute multimodel mean
    mm_min, compute multimodel minimum
    mm_max, compute multimodel maximum
    mm_stdev, compute multimodel standard deviation

Author: Jacqueline Nugent
Last Modified: November 12, 2019
"""

### TODO: need to fix how variable & model names are read in...

import warnings
import xarray as xr
import numpy as np


def area_mean(dataset, is_global=True, loc=None):
    """
    Average the data globally or across a given location for one variable,
    in some model for some scenario. Prints to the user what is being done.

    Args:
        datasets (DataSet), the preprocessed CMIP6 model data for one
                        model in some scenario for some variable; assumes
                        dimensions of latitude, longitude, and time (monthly)
        is_global (Boolean), True (default) to return the global mean;
                        False to compute the mean for a given location
        loc (list of floats), a list of the coordinate bounds of the location
                        over which the area mean will be computed; must
                        be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global mean is requested

    Returns:
        ar_mean (1D array), the time series of global or location means for
                        the dataset

    Exceptions:
        MissingLocation, raised if is_global=False but loc=None or loc is not
                        a list of length 4

    Warnings:
        LocationIgnored, given if is_global=True but loc is not None
    """
    #### compute the mean across the location or globe for each model
    model = dataset
    model_name = str(model.modelname.values)
    ntime = len(model.time)
    ar_mean = np.empty(ntime)

    ### TODO: get variable name
    #varname = model.
    varname = 'TODO'
    print('Computing area average for {var}'.format(var=varname))

    ### average the data over the lat-lon range you need:###
    # global mean, no location given:
    if is_global:

        # warn user if a location was provided anyway
        if loc is not None:
            print('\n')
            warnings.warn("Argument loc provided for global mean."
                          " Location input will be ignored and global mean"
                          " will be computed.")
        print('Averaging {var} over the globe for {name}\n'.format(
            var=varname, name=model_name))
        ar_mean[:] = model.mean(dim=['lat', 'lon'])

    # specific location:
    else:
        # raise an exception if location information was not provided
        # or is in the incorrect format
        if loc is None or len(loc) != 4:
            raise Exception('Must enter location in the form [minlon, maxlon,'
                            'minlat, maxlat]!')

        lonmin = loc[0]
        lonmax = loc[1]
        latmin = loc[2]
        latmax = loc[3]

        print(('Averaging {var} over lat {ltmn}-{ltmx}, lon {lnmn}-{lnmx} for'
               ' {name}').format(var=varname, ltmn=latmin, ltmx=latmax,
                                 lnmn=lonmin, lnmx=lonmax, name=model_name))
        ar_mean[:] = model.sel(lat=slice(latmin, latmax),
                               lon=slice(lonmin,
                                         lonmax)).mean(dim=['lat', 'lon'])

    return ar_mean


def to_xarray(stats, times):
    """
    Converts the numpy array output from one of the stats functions in this
    module to an xarray with dimension time.

    Args:
        stats (1D array), time series of the multimodel statistic
        times (1D array), array of the values for the time coordinates

    Returns:
        data (1D xarray), time series of the multimodel statistics as
                        an xarray with dimension time
    """
    data = xr.DataArray(stats, coords={'time': times}, dims=['time'])

    return data


def mm_mean(datasets, is_global=True, loc=None, xarray_out=False):
    """
    Compute the mean value of one variable, averaged over the globe or
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (Boolean), True (default) to return the global multimodel
                        mean; False to compute the multimodel mean for a given
                        location
        loc (list of floats), a list of the coordinate bounds of the location
                        over which the multimodel mean will be computed; must
                        be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global mean is requested
        xarray_out (Boolean), True to return the multimean statistic time
                        series as an xarray with dimension time;
                        False (default) to return it as a 1D numpy array

    Returns:
        multi_mean (1D array), the time series of multi-model mean of some
                        variable for some scenario; numpy array if
                        xarray_out=False; xarray if xarray_out=True
    """
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = 'TODO'
    print('Computing model area means for {var}\n'.format(var=varname))
    model_means = np.empty((nmodels, ntime))

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        model_name = str(model.modelname.values)
        print('Model {num}: {name}'.format(num=int(i+1), name=model_name))
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel mean:###
    print('Computing multimodel mean for {num} models\n'.format(num=nmodels))
    multi_mean = np.nanmean(model_means, axis=0)

    ### convert to an xarray if requested
    if xarray_out:
        multi_mean = to_xarray(multi_mean, datasets[0].time.values)

    return multi_mean


def mm_min(datasets, is_global=True, loc=None, xarray_out=False):
    """
    Compute the minimum value of one variable, globally or over
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (Boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel minimum for a
                        given location
        loc (list of floats), a list of the coordinate bounds of the location
                        over which the multimodel minimum will be computed;
                        must be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global minimum is requested
        xarray_out (Boolean), True to return the multimean statistic time
                        series as an xarray with dimension time;
                        False (default) to return it as a 1D numpy array

    Returns:
        multi_min (1D array), the time series of multi-model minimum of some
                        variable for some scenario; numpy array if
                        xarray_out=False; xarray if xarray_out=True
    """
    multi_min = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = 'TODO'
    print('Computing model area means for {var}\n'.format(var=varname))
    model_means = np.empty((nmodels, ntime))

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        model_name = str(model.modelname.values)
        print('Model {num}: {name}'.format(num=int(i+1), name=model_name))
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel minimum:###
    print('Computing multimodel minimum for {num} models\n'.format(
        num=nmodels))
    multi_min = np.min(model_means, axis=0)

    ### convert to an xarray if requested
    if xarray_out:
        multi_min = to_xarray(multi_min, datasets[0].time.values)

    return multi_min


def mm_max(datasets, is_global=True, loc=None, xarray_out=False):
    """
    Compute the maximum value of one variable, globally or over
    a given location, of one variable across the given models for one
    scenario. Prints to the user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (Boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel maximum for a
                        given location
        loc (list of floats), a list of the coordinate bounds of the location
                        over which the multimodel maximum will be computed;
                        must be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global maximum is requested
        xarray_out (Boolean), True to return the multimean statistic time
                        series as an xarray with dimension time;
                        False (default) to return it as a 1D numpy array

    Returns:
        multi_max (1D array), the time series of multi-model maximum of some
                        variable for some scenario; numpy array if
                        xarray_out=False; xarray if xarray_out=True
    """
    multi_max = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = 'TODO'
    print('Computing model area means for {var}\n'.format(var=varname))
    model_means = np.empty((nmodels, ntime))

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        model_name = str(model.modelname.values)
        print('Model {num}: {name}'.format(num=int(i+1), name=model_name))
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel maximum:###
    print('Computing multimodel maximum for {num} models\n'.format(
        num=nmodels))
    multi_max = np.max(model_means, axis=0)

    ### convert to an xarray if requested
    if xarray_out:
        multi_max = to_xarray(multi_max, datasets[0].time.values)

    return multi_max


def mm_stdev(datasets, is_global=True, loc=None, xarray_out=False):
    """
    Compute the standard deviation of one variable, averaged over the globe or
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (Boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel minimum for a
                        given location
        loc (list of floats), a list of the coordinate bounds of the location
                        over which the multimodel standard deviation will be
                        computed; must be in the form
                        [minlon, maxlon, minlat, maxlat]; None (default) if
                        global standard deviation is requested
        xarray_out (Boolean), True to return the multimean statistic time
                        series as an xarray with dimension time;
                        False (default) to return it as a 1D numpy array

    Returns:
        multi_std (1D array), the time series of multi-model standard
                        deviation of some variable for some scenario;
                        numpy array if xarray_out=False;
                        xarray if xarray_out=True
    """
    multi_stdev = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = 'TODO'
    print('Computing model area means for {var}\n'.format(var=varname))
    model_means = np.empty((nmodels, ntime))

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        model_name = str(model.modelname.values)
        print('Model {num}: {name}'.format(num=int(i+1), name=model_name))
        model_means[i, :] = area_mean(model, is_global, loc)

    ### compute standard deviation of the model area means
    print('Computing multimodel standard deviation for {num} models\n'.format(
        num=nmodels))
    multi_stdev = np.std(model_means, axis=0)

    ### convert to an xarray if requested
    if xarray_out:
        multi_stdev = to_xarray(multi_stdev, datasets[0].time.values)

    return multi_stdev