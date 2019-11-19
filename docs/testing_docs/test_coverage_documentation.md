We documented test coverage using pytest.

To reproduce our output, in terminal
> pytest --cov=Phase1_ProcessData/



### Test Coverage

We documented our test coverage using pytest.

Below is the output from running the command
> pytest --cov=Phase1_ProcessData/
from within the /local-climate-data-tool/Analysis/ folder: 

> ----------- coverage: platform linux, python 3.7.3-final-0 -----------
> Name                                                         Stmts   Miss  Cover
> --------------------------------------------------------------------------------
> Phase1_ProcessData/_test_create_data_dict.py                    47     47     0%
> Phase1_ProcessData/analysis_parameters.py                        9      0   100%
> Phase1_ProcessData/data_wrangler.py                             54     54     0%
> Phase1_ProcessData/multimodelstats.py                          113    113     0%
> Phase1_ProcessData/normalize_to_historical.py                   38     38     0%
> Phase1_ProcessData/step1_calculate_statistics.py                33     33     0%
> Phase1_ProcessData/step1_compute_global_mean_data.py            33     33     0%
> Phase1_ProcessData/subcomp_a_create_data_dict.py                14     14     0%
> Phase1_ProcessData/subcomp_a_process_climate_model_data.py      54      2    96%
> Phase1_ProcessData/subcomp_b_multi_model_stats.py               93     20    78%
> Phase1_ProcessData/test_subcomp_a.py                           137     17    88%
> Phase1_ProcessData/test_subcomp_b.py                            68     24    65%
> Phase1_ProcessData/util.py                                       5      5     0%
> --------------------------------------------------------------------------------
> TOTAL                                                          698    400    43%
