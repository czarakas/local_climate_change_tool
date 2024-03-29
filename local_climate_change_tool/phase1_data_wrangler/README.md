## Data Wrangler

In this directory, the data_wrangler.py script processes climate model and observational 
datasets (using subcomponents A-D) into processed data files for use in the Dashboard Generator.

Running this script requires access to the google-cloud-based CMIP6 data archive and a cluster
computing hub that can handle the size of these large datasets. 
**[ocean.pangeo.io](https://ocean.pangeo.io)** is an analysis hub (accessible by linking to 
your ORCID) that users can use to run this script. Note that data_wrangler.py must be run in
a notebook, i.e.:

```python
from phase1_data_wrangler import data_wrangler
data_wrangler.main()
```

The test scripts are also held in this directory and begin with the `
```python
test_<filename>.py
```
