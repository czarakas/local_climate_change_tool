import xarray as xr
import intake
import DirectoryInfo

dir_catalog=DirectoryInfo.dir_catalog

# util.py is in the local directory
# it contains code that is common across project notebooks
# or routines that are too extensive and might otherwise clutter
# the notebook design
import util 

def createDataDict(this_experiment_id, this_variable_id, this_table_id, this_grid_label):
    if util.is_ncar_host():
        col = intake.open_esm_datastore(dir_catalog+"glade-cmip6.json")
    else:
        col = intake.open_esm_datastore(dir_catalog+"pangeo-cmip6.json")
    
    cat = col.search(experiment_id=this_experiment_id, \
                     table_id=this_table_id, \
                     variable_id=this_variable_id, \
                     grid_label=this_grid_label)
    dataset_info = cat.df
    
    dset_dict = cat.to_dataset_dict(zarr_kwargs={'consolidated': True, 'decode_times': False}, 
                                cdf_kwargs={'chunks': {}, 'decode_times': False})
    #dset_dict.keys()
    
    source_ids = cat.df['source_id']
    modelnames = list(set(source_ids))
    
    return dataset_info, dset_dict, modelnames