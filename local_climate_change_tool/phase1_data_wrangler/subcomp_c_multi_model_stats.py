"""
subcomp_c_multi_model_stats.py

Generates files with multi-model statistics for each experiment.
"""
import time
import glob
import xarray as xr
import numpy as np

from phase1_data_wrangler.analysis_parameters import \
    DIR_INTERMEDIATE_PROCESSED_MODEL_DATA, EXPERIMENT_LIST, VARIABLE_ID, \
    DIR_PROCESSED_DATA


DATA_PATH = DIR_INTERMEDIATE_PROCESSED_MODEL_DATA
SCENARIO_LIST = EXPERIMENT_LIST
VARIABLE_NAME = VARIABLE_ID
OUTPUT_PATH = DIR_PROCESSED_DATA+'model_data/'
INTERMEDIATE_OUTPUT_PATH = '/home/jovyan/local-climate-data-tool/data/intermediate_data/'


def get_scenario_fnames(data_path, scenario, normalized=False):
    """ Return list of zarr files.

    Get a string list of all zarr files in the data_path for the given
    scenario.

    Args:
        data_path: The string file path.
        scenario: The string name of the scenario.
        normalized: False (default) if the model data is not normalized.
    Returns:
        names: The string list of file names.
    """
    endcut = -1*len('.zarr')
    begcut = len(data_path)
    if normalized:
        names = [f[begcut:endcut] for f in glob.glob(data_path +
                                                     'Normalized*_' + scenario + '_*.zarr')]
    else:
        names = [f[begcut:endcut] for f in glob.glob(data_path +
                                                     VARIABLE_NAME+'*_' + scenario + '_*.zarr')]
    return names


def read_in_fname(data_path, fname):
    """Read in zarr file.

    Reads in the zarr file with name datapath/fname.zarr and returns the
    correpsonding xarray.

    Args:
        data_path: The string file path.
        fname: The string file name.
    Returns:
        the opened zarr file.
    """
    filename = data_path + fname + '.zarr'
    return xr.open_zarr(filename)


def initialize_empty_mms_arrays(data_path, scenario_name, num_chunks,
                                normalized=False):
    """Initialize arrays.

    Initialize empty arrays that will hold the multi-model stats data for the
    given scenario.

    Args:
        data_path: String path where the arrays will be located.
        scenario_name: String name of the scenario.
        num_chunks: Integer number of chunks to use for saving the zarr file.
        normalized: False (default) if the data is not normalized.
    Returns:
        empty_dsets: List of empty arrays.
        dim_info: List of number of chunks (lat & lon), models, time, lat, & lon.
        dims: List containing the dimensions (lat, lon, & time).
        file_names: List of names of files containing models in the scenario.
        datasets: List of empty numpy arrays for each multi-model statistic.
    """
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
    """Fills the arrays with the multi-model statistics for that scenario.

    Args:
        empty_dsets: List of empty arrays.
        dim_info: List of number of chunks (lat & lon), models, time, lat, & lon.
        file_names: List of names of files containing models in the scenario.
        datasets: List of empty numpy arrays for each multi-model statistic.
        varname: String name of the variable.
        num_chunks: Integer number of chunks to use for saving the zarr file.
    Returns:
        List of the multi-model statistic numpy arrays (mean, min, max, std).
    """
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
    """Creates an xarray dataset from numpy arrays of multi-model statistics.

    Args:
        Arrays of dimensions (lats, lons, times) and multi-model statistic
        values (mean_vals, max_vals, min_vals, std_vals).
    Returns:
        ds: The xarray dataset of multi-model stats for the scenario.
    """
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
    """Exports dataset to a zarr file.

    Args:
        ds: The dataset to export.
        output_path: The string path of where to save the file.
        variable_name: The string name of the model variable.
        scenario_name: The string name of the scenario.
        normalized: False (default) if model data is not normalized.
    """
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
    """Create the multi-model statistics dataset for a scenario.

    Runs the function initialize_empty_mms_arrays, fill_empty_arrays,
    and create_xr_dataset to generate the multi-model statistics dataset
    for a scenario. Prints to the user what is being done.

    Args:
        variable_name: The string name of the model variable.
        scenario_name: The string name of the scenario.
        num_chunks: Integer number of chunks to use for saving the zarr file.
        data_path: String path where the arrays will be located.
        normalized: False (default) if model data is not normalized.
    Returns:
        Arrays of dimensions (lats, lons, times) and multi-model statistic
        values (mean_vals, max_vals, min_vals, std_vals).
    """

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
    """Processes all scenarios in the list.

    Calculates, exports, and creates datasets of multi-model statistics
    for all scenarios in the given list.

    Args:
        data_path: String path where the arrays will be located.
        variable_name: The string name of the model variable.
        scenario_list: String list of scenario names.
        num_chunks: Integer number of chunks to use for saving the zarr file.
        normalized: False (default) if model data is not normalized.
    """
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
