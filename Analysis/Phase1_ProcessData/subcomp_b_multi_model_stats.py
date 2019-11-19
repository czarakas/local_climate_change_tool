"""
Need to add docstring
"""

import time
import glob
import xarray as xr
import numpy as np
import analysis_parameters

DATA_PATH = analysis_parameters.DIR_INTERMEDIATE_PROCESSED_MODEL_DATA
SCENARIO_LIST = analysis_parameters.EXPERIMENT_LIST
VARIABLE_NAME = analysis_parameters.VARIABLE_ID
OUTPUT_PATH = '/home/jovyan/local-climate-data-tool/Data/ProcessedData/'
INTERMEDIATE_OUTPUT_PATH = '/home/jovyan/local-climate-data-tool/Data/IntermediateData/Multi_Model_Stats_Arrays/'

def get_scenario_fnames(data_path, scenario, normalized=False):
    """
    Get a string list of all zarr files in the data_path for the given
    scenario. Prints the list to the user.
    """
    endcut = -1*len('.zarr')
    begcut = len(data_path)
    if normalized:
        names = [f[begcut:endcut] for f in glob.glob(data_path +
                                                     'Normalized*_' + scenario + '_*.zarr')]
    else:
        names = [f[begcut:endcut] for f in glob.glob(data_path +
                                                     '*_' + scenario + '_*.zarr')]
    return names

def read_in_fname(data_path, fname):
    """Read in zarr file with name datapath/fname.zarr and return the correpsonding xarray"""
    filename = data_path + fname + '.zarr'
    return xr.open_zarr(filename)

def initialize_empty_mms_arrays(data_path, scenario_name, num_chunks,
                                normalized=False):
    """Add docstring"""
    file_names = get_scenario_fnames(data_path, scenario_name, normalized)
    datasets = [read_in_fname(data_path, x) for x in file_names]

    nmodels = len(datasets)
    times = datasets[0].time
    lats = datasets[0]['lat']
    lons = datasets[0]['lon']
    dims = [lats, lons, times]

    ntime = len(times)
    nlat = len(lats)
    nlon = len(lons)
    multi_model_means = np.empty((ntime, nlat, nlon))
    multi_model_maxs = np.empty((ntime, nlat, nlon))
    multi_model_mins = np.empty((ntime, nlat, nlon))
    multi_model_stds = np.empty((ntime, nlat, nlon))

    chunk_size = int(nlat/num_chunks)

    boundary_cond = np.zeros(num_chunks)
    boundary_cond[num_chunks-1] = -(chunk_size*num_chunks)+nlat

    nlat0_chunk = chunk_size*np.arange(0, num_chunks)
    nlatf_chunk = chunk_size*np.arange(1, num_chunks+1) +boundary_cond

    empty_dsets = [multi_model_means, multi_model_mins, multi_model_maxs, multi_model_stds]
    dim_info = [nlat0_chunk, nlatf_chunk, nmodels, ntime, nlat, nlon]

    return [empty_dsets, dim_info, dims, file_names, datasets]

def fill_empty_arrays(empty_dsets, dim_info, file_names, datasets, varname, num_chunks):
    """Add docstring"""
    [multi_model_means,
     multi_model_mins,
     multi_model_maxs,
     multi_model_stds] = empty_dsets
    [nlat0_chunk, nlatf_chunk, nmodels, ntime, _, nlon] = dim_info
    for c in range(0, num_chunks):
        # Define bounds for data chunk
        nlat0 = int(nlat0_chunk[c])
        nlatf = int(nlatf_chunk[c])
        nlat_chunk = nlatf - nlat0

        # Get data chunk from all models
        model_data_chunk = np.empty((nmodels, ntime, nlat_chunk, nlon))
        for i in range(nmodels):
            #model_name = file_names[i].split("_")[2]
            #print(model_name)
            model_data_chunk[i, :, :, :] = datasets[i][varname][:, nlat0:nlatf, :]

        multi_mean_chunk = np.nanmean(model_data_chunk, axis=0)
        multi_min_chunk = np.nanmin(model_data_chunk, axis=0)
        multi_max_chunk = np.nanmax(model_data_chunk, axis=0)
        multi_std_chunk = np.nanstd(model_data_chunk, axis=0)

        multi_model_means[:, nlat0:nlatf, :] = multi_mean_chunk
        multi_model_mins[:, nlat0:nlatf, :] = multi_min_chunk
        multi_model_maxs[:, nlat0:nlatf, :] = multi_max_chunk
        multi_model_stds[:, nlat0:nlatf, :] = multi_std_chunk

    return [multi_model_means, multi_model_mins,
            multi_model_maxs, multi_model_stds]

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

def export_dataset(ds, output_path, variable_name, scenario_name, normalized=False):
    """Exports dataset to zarr file"""
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    if normalized:
        ds.to_zarr(output_path+'modelData_normalized_'+
                   variable_name+'_'+scenario_name+'.zarr')
    else:
        ds.to_zarr(output_path+'modelData_'+
                   variable_name+'_'+scenario_name+'.zarr')

def create_scenario_mms_datasets(variable_name,
                                 scenario_name,
                                 num_chunks,
                                 data_path,
                                 normalized=False):
    """Add docstring"""

    print('Creating empty arrays')
    [empty_dsets,
     dim_info,
     dims,
     file_names,
     datasets] = initialize_empty_mms_arrays(data_path,
                                             scenario_name=scenario_name,
                                             num_chunks=20,
                                             normalized=normalized)
    [lats, lons, times] = dims

    print('Calculating multimodel statistics')
    [mean_vals,
     min_vals,
     max_vals,
     std_vals] = fill_empty_arrays(empty_dsets,
                                   dim_info,
                                   file_names,
                                   datasets,
                                   variable_name,
                                   num_chunks)


    print('Exporting dataset')
    ds = create_xr_dataset(lats, lons, times, mean_vals, max_vals, min_vals, std_vals)

    export_dataset(ds=ds,
                   output_path=OUTPUT_PATH,
                   variable_name=variable_name,
                   scenario_name=scenario_name,
                   normalized=normalized)

    return lats, lons, times, mean_vals, max_vals, min_vals, std_vals


#------------------MAIN WORKFLOW----------------------------------------
def process_all_scenarios(data_path, variable_name, scenario_list,
                          num_chunks=20, normalized=False):
    for scenario_name in scenario_list:
        print('-----------'+scenario_name+'-----------')
        start_time = time.time()
        [lats,
         lons,
         times,
         mean_vals,
         max_vals,
         min_vals,
         std_vals] = create_scenario_mms_datasets(data_path=data_path,
                                                  variable_name=variable_name,
                                                  scenario_name=scenario_name,
                                                  num_chunks=num_chunks,
                                                  normalized=normalized)
        end_time = time.time()
        print(end_time - start_time)
