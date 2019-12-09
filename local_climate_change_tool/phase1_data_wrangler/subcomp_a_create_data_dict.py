"""
subcomp_a_create_data_dict.py

Creates a data dictionary for the climate model databased on the analysis
parameters.
"""

import intake
from phase1_data_wrangler.analysis_parameters import DIR_CATALOG


def create_data_dict(this_experiment_id, this_variable_id,
                     this_table_id, this_grid_label):
    """Creates data dictionary.

    Creates a data dictionary for some variable, grid, and table id for
    the chosen experiment(s).

    Args:
        this_experiment_id: The string ID for the experiment.
                            Can be list of strings.
        this_variable_id; The string ID for this variable (e.g. 'tas').
        this_table_id: ID for the table (e.g. 'Amon').
        this_grid_label: String label of the reference grid (e.g. 'gn').
    Returns:
        dataset_info:
        dset_dict: The data dictionary.
        modelnames: String list of source ids of the models in the dict.
    """
    col = intake.open_esm_datastore(DIR_CATALOG + "pangeo-cmip6.json")

    cat = col.search(experiment_id=this_experiment_id,
                     table_id=this_table_id,
                     variable_id=this_variable_id,
                     grid_label=this_grid_label)
    dataset_info = cat.df

    dset_dict = cat.to_dataset_dict(zarr_kwargs={'consolidated': True,
                                                 'decode_times': False},
                                    cdf_kwargs={'chunks': {},
                                                'decode_times': False})
    source_ids = cat.df['source_id']
    modelnames = list(set(source_ids))

    return dataset_info, dset_dict, modelnames
