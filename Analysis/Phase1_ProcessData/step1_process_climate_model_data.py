"""
This module processes raw CMIP6 output to create files with consistent dimensions for all models.

Running this script for all models with just averaging over ensembles, regridding, and saving takes about 15-20 mins.

Make sure to clear the directory you would like the zarr files to be saved in - something about
this format makes it not work to overwrite existing files.
"""

####################### Load Packages ########################################

import time
import cftime
import xarray as xr
import xesmf as xe

import analysis_parameters
import create_data_dict

############ Read in Settings for Data Dictionary#############################

THIS_EXPERIMENT_ID = analysis_parameters.EXPERIMENT_LIST
THIS_VARIABLE_ID = analysis_parameters.VARIABLE_ID
THIS_TABLE_ID = analysis_parameters.TABLE_ID
THIS_GRID_LABEL = analysis_parameters.GRID_LABEL
OUTPUT_PATH = analysis_parameters.DIR_PROCESSED_DATA
DIR_INTERMEDIATE = analysis_parameters.DIR_INTERMEDIATE_DATA

########### Create Data Dictionary to test####################################

# each value in this dictionary is an xarray with dimensions:
# lat, lon, time, member_id

[DATASET_INFO,
 DSET_DICT,
 MODELNAMES] = create_data_dict.create_data_dict(THIS_EXPERIMENT_ID,
                                                 THIS_VARIABLE_ID,
                                                 THIS_TABLE_ID,
                                                 THIS_GRID_LABEL)

########### Create functions for analysis ####################################

def create_reference_grid(modelname, experiment_id, activity_id):
    """Creates reference grid to which all model output will be regridded"""
    dataset_info_subset = DATASET_INFO[DATASET_INFO['source_id'] == modelname]
    institution_id = list(set(dataset_info_subset['institution_id']))[0]
    nametag = activity_id+'.'+institution_id+'.'+modelname+'.'+experiment_id+\
              '.'+THIS_TABLE_ID+'.'+THIS_GRID_LABEL
    thisdata = DSET_DICT[nametag]
    ds_out = xr.Dataset({'lat': thisdata['lat'],
                         'lon': thisdata['lon']})
    return ds_out

def reindex_time(startingtimes):
    """Reindexes time series to proleptic Gregorian calendar type"""
    newtimes = startingtimes.values
    for i in range(0, len(startingtimes)):
        yr = int(str(startingtimes.values[i])[0:4])
        mon = int(str(startingtimes.values[i])[5:7])
        newdate = cftime.DatetimeProlepticGregorian(yr, mon, 15)
        newtimes[i] = newdate
    return newtimes

def regrid_model(ds, reference_grid, latvariable='lat', lonvariable='lon'):
    """Regrids model output to a reference grid"""
    data_series = ds[THIS_VARIABLE_ID]
    ds_in = xr.Dataset({'lat': data_series[latvariable],
                        'lon': data_series[lonvariable],
                        'time': data_series['time'],
                        THIS_VARIABLE_ID: data_series})
    regridder = xe.Regridder(ds_in, reference_grid, 'nearest_s2d')
    data_series_regridded = regridder(ds_in)
    data_series_regridded.attrs.update(data_series.attrs)
    return data_series_regridded

def process_dataset(this_key):
    """ Processes each dataset in dictionary
    This processing involves:
        (1) Averaging over all ensemble members (member ids)
        (2) Getting into consistent time format
        (3) Renaming coordinates if necessary
        (4) Regridding to reference dataset
    """
    # Get original dataset from dictionary
    ds_original = DSET_DICT[this_key]

    # Average over all ensemble members
    ds = ds_original.mean(dim=['member_id'])

    # Reindex time to consistent time datatype
    ds = xr.decode_cf(ds)
    newtimes = reindex_time(startingtimes=ds['time'])
    ds['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])

    # Rename latitude and longitude coordinate names if necessary
    if 'latitude' in ds.dims:
        ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
    else:
        pass

    # Regrid dataset to reference grid
    dataset_regridded = regrid_model(ds, FINAL_GRID)

    return dataset_regridded

def generate_new_filename(this_key):
    """Generates filename for processed data"""
    [_, _, source_id, experiment_id, _, _] = this_key.split('.')
    this_fname = THIS_VARIABLE_ID+'_'+experiment_id+'_'+source_id
    return this_fname

def save_dataset(ds, this_fname):
    """Saves processed dataset as zarr file"""
    ds.load()
    # Export intermediate processed dataset as zarr file
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(DIR_INTERMEDIATE+this_fname+'.zarr')


##################### Main Workflow ##########################################

FINAL_GRID = create_reference_grid(modelname='CAMS-CSM1-0',
                                   activity_id='CMIP',
                                   experiment_id='historical')

for key in DSET_DICT.keys():
    # Generate new filename for intermediate processed data
    fname = generate_new_filename(key)

    # Check if one of cases that throws exceptions (to investigate later)
    if fname in ('tas_historical_CESM2',
                 'tas_ssp126_CanESM5',
                 'tas_ssp126_CAMS-CSM1-0',
                 
                 'tas_ssp245_CAMS-CSM1-0',
                 'tas_ssp245_HadGEM3-GC31-LL',
                 
                 'tas_ssp370_CESM2-WACCM',
                 'tas_ssp370_MPI-ESM1-2-HR',
                 'tas_ssp370_CAMS-CSM1-0',
                 'tas_ssp370_BCC-ESM1',
                 
                 'tas_ssp585_CAMS-CSM1-0',
                 'tas_ssp585_CanESM5'
                ):
        print('******** skipping ************')
    else:
        # Process data
        ds_processed = process_dataset(key)

        # Save processed data
        save_dataset(ds_processed, fname)
