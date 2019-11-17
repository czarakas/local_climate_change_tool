import time
import pickle
import analysis_parameters
import xarray as xr
import glob
import numpy as np
import matplotlib.pyplot as plt
import multimodelstats as mms

DATA_PATH = analysis_parameters.DIR_INTERMEDIATE_DATA+'Processed_Model_Data/'
SCENARIO_LIST = analysis_parameters.EXPERIMENT_LIST
VARIABLE_NAME = analysis_parameters.VARIABLE_ID
OUTPUT_PATH = '/home/jovyan/local-climate-data-tool/Data/ProcessedData/'
INTERMEDIATE_OUTPUT_PATH='/home/jovyan/local-climate-data-tool/Data/IntermediateData/Multi_Model_Stats_Arrays/'

def get_scenario_fnames(data_path, scenario):
    """
    Get a string list of all zarr files in the data_path for the given 
    scenario. Prints the list to the user.
    """
    endcut = -1*len('.zarr')
    begcut = len(data_path)
    names = [f[begcut:endcut] for f in glob.glob(data_path + '*_' + scenario + '_*.zarr')]
    return names

def read_in_fname(data_path, fname):
    """Read in zarr file with name datapath/fname.zarr and return the correpsonding xarray"""
    filename = data_path + fname + '.zarr'
    return xr.open_zarr(filename)

def initialize_empty_mms_arrays(data_path, initial_ds_fname, variable_name):
    """Creates an empty numpy array with the correct dimensions based on
    the shape of a single processed model data file"""
    ds_init = read_in_fname(data_path, initial_ds_fname)
    ds_init.load()
    ds_dims = np.shape(ds_init[variable_name].values)
    lats = ds_init['lat']
    lons = ds_init['lon']
    times = ds_init['time']
    
    empty_array = np.empty(ds_dims)

    mean_vals = np.copy(empty_array)
    max_vals = np.copy(empty_array)
    min_vals = np.copy(empty_array)
    std_vals = np.copy(empty_array)
    
    return lats, lons, times, mean_vals, max_vals, min_vals, std_vals

def save_incomplete_dataset(output_path_temp, fname_temp, mean_vals, min_vals, max_vals, std_vals):
    """Save multi-model mean numpy arrays as pickle files. This is useful
    for saving partially-filled (incomplete) numpy arrays midway through analysis"""
    with open(output_path_temp+fname_temp+'_mean'+'.pickle', 'wb') as handle:
        pickle.dump(mean_vals, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(output_path_temp+fname_temp+'_min'+'.pickle', 'wb') as handle:
        pickle.dump(min_vals, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(output_path_temp+fname_temp+'_max'+'.pickle', 'wb') as handle:
        pickle.dump(max_vals, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(output_path_temp+fname_temp+'_std'+'.pickle', 'wb') as handle:
        pickle.dump(std_vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def fill_mms_arrays(scenario_name, lats, lons, mean_vals, min_vals, max_vals, std_vals,
                    start_lat, end_lat):
    """Fills empty numpy arrays with multi-model statics by iterating through
    each grid cell and calculating multi-model stastics at each grid cell"""
    file_names_hist = get_scenario_fnames(DATA_PATH, scenario_name)
    datasets_hist = [read_in_fname(DATA_PATH, fname) for fname in file_names_hist]
    start_time = time.time()
    for i in range(start_lat, end_lat):
        lt = lats.values[i]
        print('calculating stats for '+str(i))
        for j in range(0,len(lons.values)):
            ln = lons.values[j]
            stats_single_point = mms.export_stats(datasets_hist, file_names_hist, is_global_mean=False, coords=[lt, ln])
            mean_vals[:,i,j] = stats_single_point['multi_mean'].values
            min_vals[:,i,j] = stats_single_point['multi_min'].values
            max_vals[:,i,j] = stats_single_point['multi_max'].values
            std_vals[:,i,j] = stats_single_point['multi_std'].values
        end_time = time.time()
        print(str(i)+' complete')
        print(end_time - start_time)
        
        # Save temporary files every 10 latitude bands
        if np.mod(i,10)==0:
            save_incomplete_dataset(output_path_temp=INTERMEDIATE_OUTPUT_PATH,
                                    fname_temp='temporary_multi_model_stats_grid_'+scenario_name,
                                    mean_vals=mean_vals,
                                    min_vals=min_vals,
                                    max_vals=max_vals,
                                    std_vals=std_vals)

    return mean_vals, min_vals, max_vals, std_vals

def create_xr_dataset(lats, lons, times, mean_vals, max_vals, min_vals, std_vals):
    """Creates an xarray dataset from numpy arrays of multi-model statics"""
    # Create xarrays from numpy array
    ds_coords = {'time': times, 'lat': lats, 'lon': lons}
    ds_dims = ('time', 'lat', 'lon')
    mean_xr = xr.DataArray(mean_vals, dims=ds_dims, coords=ds_coords)
    max_xr = xr.DataArray(max_vals, dims=ds_dims, coords=ds_coords)
    min_xr = xr.DataArray(min_vals, dims=ds_dims, coords=ds_coords)
    std_xr = xr.DataArray(std_vals, dims=ds_dims, coords=ds_coords)
    
    # Create xarray dataset from xarrays
    ds = xr.Dataset({'mean': mean_xr,
                     'min': min_xr,
                     'max': max_xr,
                     'std': std_xr,},
                    coords=ds_coords)

    return ds

def export_dataset(ds, output_path, variable_name, scenario_name):
    """Exports dataset to zarr file"""
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(output_path+'modelData_'+variable_name+'_'+scenario_name+'.zarr')
    
def create_scenario_mms_datasets(data_path,
                                 variable_name,
                                 scenario_name,
                                 modelname_init='UKESM1-0-LL'):
    
    initial_ds_fname = variable_name+'_'+scenario_name+'_'+modelname_init
    [lats, lons, times,
     mean_vals, max_vals,
     min_vals, std_vals] = initialize_empty_mms_arrays(data_path,
                                                       initial_ds_fname,
                                                       variable_name)
    
    [mean_vals, min_vals,
     max_vals, std_vals] = fill_mms_arrays(scenario_name=scenario_name,
                                           lats=lats, lons=lons,
                                           mean_vals=mean_vals, min_vals=min_vals,
                                           max_vals=max_vals, std_vals=std_vals,
                                           start_lat=0, end_lat=len(lats.values))

    
    ds = create_xr_dataset(lats, lons, times, mean_vals, max_vals, min_vals, std_vals)
    
    export_dataset(ds=ds,
                   output_path=OUTPUT_PATH,
                   variable_name=variable_name,
                   scenario_name=scenario_name)
    
    return lats, lons, times, mean_vals, max_vals, min_vals, std_vals
    
    