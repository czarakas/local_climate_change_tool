### Testing Approach
This folder contains a screenshot summarizing our testing process for this project.

We wrote 5 unit tests for the Data Wrangler module of our package, each of which contained multiple functions which tested various aspects of our code and workflow including checking that:
* datasets and dictionaries we created were not empty
* datasets have the expected column names
* dataset columns are expected data types, and that entries in the columns are consistent
* dimensions (lat, lon, time) of our processed datasets are all consistent with each other
* our regridding and time reindexing functions work as expected on test datasets (e.g. 1/1/2019 in 360-day model calendar stays 1/1/2019 in Gregorian calendar)
* exporting datasets to different file types (e.g. zarr) and reimporting them maintains datasets' dimensions and data types
* summary statistics in processed data sets are in logical order (e.g. minimum < mean < maximum)
* processed datasets do not contain nans

Our Data Wrangler module passed all tests and testing achieved 82% coverage, as documented below. Because our tests involve manipulating large datasets and being connected to the climate model data server, it was not feasible to run the majority of our testing on Travis.  We also did not write tests for the Dashboard Generator module  based on input from Dave on 11/18/2019 that this was "beyond the scope of this class" and not necessary for our final project. 

### Folder Contents:

* **Data_Wrangler_Test_Coverage_Screenshot.png**: This is a screenshot of pytests' assessment of our test coverage. To reproduce this screenshot, you can run the following command from within the **/local_climate_change_tool/local_climate_change_tool/** folder:

> pytest --cov=phase1_data_wrangler

