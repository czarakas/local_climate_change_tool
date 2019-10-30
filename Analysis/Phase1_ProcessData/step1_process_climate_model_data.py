"""
This module processes raw CMIP6 output to create files with consistent dimensions for all models
"""

######## Load Packages
import xarray as xr
import xesmf as xe

import analysis_parameters
import create_data_dict

######### Read in Settings for Data Dictionary
THIS_EXPERIMENT_ID = analysis_parameters.EXPERIMENT_LIST
THIS_VARIABLE_ID = analysis_parameters.VARIABLE_ID
THIS_TABLE_ID = analysis_parameters.TABLE_ID
THIS_GRID_LABEL = analysis_parameters.GRID_LABEL
OUTPUT_PATH = analysis_parameters.DIR_PROCESSED_DATA
DIR_INTERMEDIATE = '/home/jovyan/local-climate-data-tool/Data/IntermediateData/'

######### Create Data Dictionary to test
[DATASET_INFO,
 DSET_DICT,
 MODELNAMES] = create_data_dict.create_data_dict(THIS_EXPERIMENT_ID,
                                                 THIS_VARIABLE_ID,
                                                 THIS_TABLE_ID,
                                                 THIS_GRID_LABEL)

def create_reference_grid(modelname, experiment_id, activity_id):
    """Creates reference grid to which all model output will be regridded"""
    dataset_info_subset = DATASET_INFO[DATASET_INFO['source_id'] == modelname]
    institution_id = list(set(dataset_info_subset['institution_id']))[0]
    nametag = activity_id+'.'+institution_id+\
              '.'+modelname+'.'+experiment_id+\
              '.'+THIS_TABLE_ID+'.'+THIS_GRID_LABEL
    thisdata = DSET_DICT[nametag]
    ds_out = xr.Dataset({'lat': thisdata['lat'],
                         'lon': thisdata['lon']})
    return ds_out

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
    """Processes each dataset in dictionary
    This processing involves:
        (1) Averaging over all ensemble members (member ids)
        (2) Regridding to reference dataset
        (3) Getting into consistent time format (NOT IMPLEMENTED YET)
    """
    # Get original dataset from dictionary
    ds_original = DSET_DICT[this_key]

    # Average over all ensemble members
    ds = ds_original.mean(dim=['member_id'])

    # Regrid dataset to reference grid
    dataset_regridded = regrid_model(ds, FINAL_GRID)
    
    # Reindex time to consistent time datatype
    # NEED TO DO!

    return dataset_regridded

def generate_new_filename(this_key):
    [_, _, source_id, experiment_id, _, _] = key.split('.')
    fname = THIS_VARIABLE_ID+'_'+experiment_id+'_'+source_id
    return fname

def save_dataset(ds, fname):
    ds.load()
    
    # Export intermediate processed dataset as zarr file
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(DIR_INTERMEDIATE+fname+'.zarr')
    

###############################

FINAL_GRID = create_reference_grid(modelname='CAMS-CSM1-0',
                                   activity_id='CMIP',
                                   experiment_id='historical')

for key in DSET_DICT.keys():
    # Generate new filename for intermediate processed data
    fname = generate_new_filename(key)
    print(fname)

    # Process data
    ds_processed = process_dataset(key)

    # Save processed data
    save_dataset(ds_processed, fname)
