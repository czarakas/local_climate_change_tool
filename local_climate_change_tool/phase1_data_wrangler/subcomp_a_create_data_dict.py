"""
Creates data dictionary based on analysis parameters
"""

import intake
from phase1_data_wrangler.analysis_parameters import DIR_CATALOG


def create_data_dict(this_experiment_id, this_variable_id,
                     this_table_id, this_grid_label):
    """
    Creates data dictionary
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
