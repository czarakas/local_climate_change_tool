"""
Module to compute multimodel statistics.

***CURRENTLY UNDERGOING TESTING***

Functions:
    area_mean, average model data over some location
    mm_mean, compute multimodel mean
    mm_min, compute multimodel minimum
    mm_max, compute multimodel maximum
    mm_stdev, compute multimodel standard deviation

Author: Jacqueline Nugent
Last Modified: November 12, 2019
"""

import warnings
import numpy as np


def area_mean(dataset, is_global=True, loc=None):
    """
    Average the data globally or across a given location for one variable,
    in some model for some scenario. Prints to the user what is being done.

    Args:
        datasets (DataSet), the preprocessed CMIP6 model data for one
                        model in some scenario for some variable; assumes
                        dimensions of latitude, longitude, and time (monthly)
        is_global (boolean), True (default) to return the global mean;
                        False to compute the mean for a given location
        loc (list of strings), a list of the coordinate bounds of the location
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
    ### TODO: adjust data extraction as needed for specific structure
    ### of the pre-processed data

    #### compute the mean across the location or globe for each model
    model = dataset
    ntime = len(model.time)
    ar_mean = np.empty(ntime)

    ### TODO: get variable name
    #varname = model.
    varname = "TODO"
    print('Computing area average for %s') %(varname)
    print 'Number time steps: ' + str(ntime)

    ### average the data over the lat-lon range you need:###
    # global mean, no location given:
    if is_global:

        # warn user if a location was provided anyway
        if loc is not None:
            warnings.warn("Argument loc provided for global mean." +
                          " Location input will be ignored and global mean will be computed.")
        print('Averaging %s over the globe for %s') %(varname, model.modelname)
        ar_mean[:] = model.mean(dim=['lat', 'lon'])

    # specific location:
    else:
        # raise an exception if location information was not provided
        # or is in the incorrect format
        if loc is None or len(loc) != 4:
            raise Exception('Must enter location in the form [minlon, maxlon, minlat, maxlat]!')

        lonmin = loc[0]
        lonmax = loc[1]
        latmin = loc[2]
        latmax = loc[3]

        print ('Averaging {var} over lat {ltmn}-{ltmx}, lon {lnmn}-{lnmx} for'
               '{model}').format(var=varname, ltmn=latmin, ltmx=latmax,
                                 lnmn=lonmin, lnmx=lonmax, model=model.modelname)
        ar_mean[:] = model.sel(lat=slice(latmin, latmax), lon=slice(lonmin, lonmax)).mean()

    return ar_mean


def mm_mean(datasets, is_global=True, loc=None):
    """
    Compute the mean value of one variable, averaged over the globe or
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (boolean), True (default) to return the global multimodel mean;
                        False to compute the multimodel mean for a given
                        location
        loc (list of strings), a list of the coordinate bounds of the location
                        over which the multimodel mean will be computed; must
                        be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global mean is requested

    Returns:
        multi_mean (1D array), the time series of multi-model mean of some
                        variable for some scenario
    """
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = "TODO"
    print('Computing model area means for %s\n') %(varname)
    model_means = np.empty((nmodels, ntime))

    ### TODO: adjust data extraction as needed for specific structure
    ### of the pre-processed data

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        print('Model %d: %s') %(int(i+1), model.modelname)
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel mean:###
    print('Computing multimodel mean for %d models.\n') %(nmodels)
    multi_mean = np.nanmean(model_means, axis=0)

    return multi_mean


def mm_min(datasets, is_global=True, loc=None):
    """
    Compute the minimum value of one variable, globally or over
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel minimum for a
                        given location
        loc (list of strings), a list of the coordinate bounds of the location
                        over which the multimodel minimum will be computed;
                        must be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global minimum is requested

    Returns:
        multi_min (1D array), the time series of multi-model minimum of some
                        variable for some scenario
    """
    multi_min = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = "TODO"
    print('Computing model area means for %s\n') %(varname)
    model_means = np.empty((nmodels, ntime))

    ### TODO: adjust data extraction as needed for specific structure
    ### of the pre-processed data

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        print('Model %d: %s') %(int(i+1), model.modelname)
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel minimum:###
    print('Computing multimodel minimum for %d models.\n') %(nmodels)
    multi_min = np.min(model_means, axis=0)

    return multi_min


def mm_max(datasets, is_global=True, loc=None):
    """
    Compute the maximum value of one variable, globally or over
    a given location, of one variable across the given models for one
    scenario. Prints to the user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel maximum for a
                        given location
        loc (list of strings), a list of the coordinate bounds of the location
                        over which the multimodel maximum will be computed;
                        must be in the form [minlon, maxlon, minlat, maxlat];
                        None (default) if global maximum is requested

    Returns:
        multi_max (1D array), the time series of multi-model maximum of some
                        variable for some scenario
    """
    multi_max = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = "TODO"
    print('Computing model area means for %s\n') %(varname)
    model_means = np.empty((nmodels, ntime))

    ### TODO: adjust data extraction as needed for specific structure
    ### of the pre-processed data

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        print('Model %d: %s') %(int(i+1), model.modelname)
        model_means[i, :] = area_mean(model, is_global, loc)

    ### multimodel maximum:###
    print('Computing multimodel maximum for %d models.\n') %(nmodels)
    multi_max = np.max(model_means, axis=0)

    return multi_max


def mm_stdev(datasets, is_global=True, loc=None):
    """
    Compute the standard deviation of one variable, averaged over the globe or
    a given location, across the given models for one scenario. Prints to the
    user what is being done.

    Args:
        datasets (list of DataSets), the preprocessed CMIP6 model data with
                        separate DataSets for each model in some scenario for
                        some variable; assumes dimensions of latitude,
                        longitude, and time (monthly)
        is_global (boolean), True (default) to return the global multimodel
                        minimum; False to compute the multimodel minimum for a
                        given location
        loc (list of strings), a list of the coordinate bounds of the location
                        over which the multimodel standard deviation will be
                        computed; must be in the form
                        [minlon, maxlon, minlat, maxlat]; None (default) if
                        global standard deviation is requested

    Returns:
        multi_std (1D array), the time series of multi-model standard
                        deviation of some variable for some scenario
    """
    multi_stdev = 0.0
    nmodels = len(datasets)
    ntime = len(datasets[0].time)
    ### TODO: get variable name
    #varname = model.
    varname = "TODO"
    print('Computing model area means for %s\n') %(varname)
    model_means = np.empty((nmodels, ntime))

    #### compute the mean across the location or globe for each model
    for i in range(nmodels):
        model = datasets[i]
        print('Model %d: %s') %(int(i+1), model.modelname)
        model_means[i, :] = area_mean(model, is_global, loc)

    ### compute standard deviation of the model area means
    print('Computing multimodel standard deviation for %d models.\n') %(nmodels)
    multi_stdev = np.std(model_means, axis=0)

    return multi_stdev