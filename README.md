[![GitHub contributors](https://img.shields.io/github/contributors/czarakas/local_climate_change_tool)](#contributors) 
[![Build Status](https://travis-ci.org/czarakas/local_climate_change_tool.svg?branch=master)](https://travis-ci.org/czarakas/local_climate_change_tool)
[![GitHub license](https://img.shields.io/github/license/czarakas/local_climate_change_tool)](https://github.com/czarakas/local_climate_change_tool/blob/master/LICENSE)

# Local Climate Change Tool
This local climate data tool displays the data from CMIP-6 output for historical
and four different future scenarios via the Shared Socioeconomic Pathways (SSPs)
described below. The motivation for this tool is to make climate data more
accessible to people with little to no computing knowledge or background in
atmospheric science or climate studies.

#### SSPs
Climate models were run for different future scenarios which represent different shared socioeconomic 
pathways (SSPs), which make projections on what would happen in the future based on various 
assumptions of human activity, e.g. how much carbon-based energy is used and the amount of
carbon emissions, assuming no further climate change or changing policies. In the order of
most to least sustainable, these assumptions are SSP1: Sustainability, SSP2: Middle-of-the-road,
SSP3: Regional Rivalry, and SSP5: Fossil Fueled Development.

For this project, we implemented data from the class of 21st century scenarios (Tier 1) listed 
below ranging from highest to lowest
emission scenarios.

1. SSP5: Fossil-Fueled Development
1. SSP3: Regional Rivalry
1. SSP2: Middle of the Road
1. SSP1: Sustainability


*See [here](https://doi.org/10.5194/gmd-9-1937-2016) for a very detailed explanation.*

#### Historical
The CMIP6 data has a modeled version of historical data - the models were run for a historical
experiment to recreate the past to validate the models. We also use historical temperature observations
that come from the Berkeley Earth Surface Temperature (BEST) dataset, which consists of monthly means 
of land surface air temperature observations that have been structured onto a 1° x 1° latitude-longitude grid,
although observations may not be available for every point on the grid at all time steps. For more information, visit
[http://berkeleyearth.org/](http://berkeleyearth.org/).

1. Modeled Historical: CMIP6 historical simulation
1. Observed Historical: data from Berkeley Earth Surface Temperatures ([BEST](http://berkeleyearth.org/about-data-set/))

## User Guide
Install package by cloning this repository then running setup.py in this current directory. The package consists of two main components: the **data wrangler** and the **dashboard generator** (documented in more detail in the Component Specification). Because running the data wrangler requires access to large raw climate model datasets, and we would like users to be able to launch the dashboard without navigating a high performance computing system, we have uploaded the processed datasets that are output by the data wrangler to google drive and included a script to download that already processed data.
We recommend users configure their python environments following step 2 of the User Guide located in the examples folder ([`examples/User_guide.pdf`](examples/User_Guide.pdf)). This will ensure that all packages necessary for the data to be processed and the panel to be run are installed correctly.
The User Guide also contains more instructions on how to use the climate dashboard.

Created by a team of researchers at the University of Washington. For bugs and
issues, report them [here](https://github.com/czarakas/local-climate-data-tool/issues).

## Directory Hierarchy
This section describes the set up of the directories in this repository.

```bash
├── LICENSE
├── README.md
├── data/
│   ├── catalogs/
│   ├── files_for_testing/
│   ├── intermediate_processed_data/
│   └── processed_data/
├── docs/
│   ├── Component_Specification.pdf
│   ├── Data_Description.pdf
│   ├── Final_Presentation_Dec_4.pdf
│   ├── Functional_specs.pdf
│   ├── TechnologyReview.pptx
│   ├── testing_docs/
|   ├── Cover_Sheet.pdf
|   └── pylint_scores/
├── environment.yml
├── examples/
│   └── User_guide.pdf
├── local_climate_change_tool
│   ├── Phase1_User_Interface.ipynb
│   ├── download_file_from_google_drive.py
│   ├── phase1_data_wrangler
│   └── phase2_dashboard_generator
├── requirements.txt
└── setup.py
```

#### Directory
Within the ```local_climate_change_tool/``` directory, ```phase1_data_wrangler/``` is responsible
for processing the raw model output into a format that is uniform and easily read by the
dashboard app. The code that creates the climate dashboard with which the user can interact
is contained within the ```phase2_dashboard_generator/``` directory. 

The ```data/``` holds folders to hold the data from CMIP6 (scenario models and historical model),
BEST (historical reanalysis data), and some smaller data files for testing. These directories
are initially empty and will be populated when the data_wrangler is run or when processed files
are downloaded from the google drive.

The documentation for this project including Functional and Component Specifications, and class
presentations for CSE583 is in ```docs/```. 
This documentation includes an overview of our project structure and details on where and how we have met each of the project requirements contained in the **Cover Sheet** ([`docs/Cover_Sheet.pdf`](docs/Cover_Sheet.pdf)). The Cover Sheet also explains the software engineering lessons we have learned throughout this process.
The ```docs/``` subdirectory also contains a folder ([`docs/pylint_scores/`](docs/pylint_scores/)) with screenshots of our successful ```pylint``` runs and details of the overall score for our package.

For a easy-to-follow guide and instructions to set up the ***Local Climate Change Tool***, see
the ```examples/User``` directory. 

#### Other Important Files
**environment.yml**: contains dependencies for you to install the conda environment 
used for this project. 
    
**requirements.txt**: contains extra dependencies to install using `pip` inside the created environment as outlined in the User Guide ([`examples/User_guide.pdf`](examples/User_Guide.pdf)). 

### How to Install the Local Climate Change Tool
#### Step 1: Create your environment
Run the following commands from the terminal to create the environment. 

```
    conda create --name climate_tool
    conda activate climate_tool
    conda install pip
    pip install -r requirements.txt
    python setup.py install --user
```

#### Step 2: Download/Generate the processed climate data
Follow the instructions in 
[```local_climate_change_tool/Phase1_User_Interface.ipynb```](local_climate_change_tool/Phase1_User_Interface.ipynb)
by doing either of the following:
- **Option 1**: Download data from google drive as shown in the script above.
- **Option 2**: Run the data_wrangler module manually which will automatically incorporates
    the most up-to-date datasets on the google-cloud-based Coupled Model Intercomparison 
    Project Phase 6 (CMIP6) data archive. 

#### Step 3: Run the climate dashboard
Follow the instructions [here](local_climate_change_tool/phase2_dashboard_generator/README.md).
Generate the climate dashboard app by running the 
[climate_dashboard](local_climate_change_tool/phase2_dashboard_generator/climate_dashboard.ipynb)
notebook or opening it in a new window by using the command line prompt:

```panel serve --show climate_dashboard.ipynb```

#### Step 4: Interact with the data through the dashboard app
The [userguide](examples/User_guide.pdf) shows instructions on how to interact with the data using 
the climate dashboard.

## Future Directions
- Create display map of selected region and surroundings so that users can visualize the scale
    from which this data is coming. Another step is to allow users to interact with the map
    so that the plots update based on latitude and longitude of user's click.
- We would like to add more variables to this interactive panel as well such as precipitation.
- Add options to visualize seasonal or monthly means
- Incorporate an option to visualize a running mean, 5 year mean, or the like.
- Use all models that are a part of CMIP6. This package allows you to incorporate more models as
    they are uploaded/added to CMIP6. 
- Make a feature to toggle between absolute temperature and temperature differences from pre-industrial era. 
    they are uploaded/added to CMIP6.

## Contributors
Thanks to the following people for their work on this project.
- @smturbev
- @czarakas
- @jacnugent
- @ihsankahveci
- @lesnyder

## Acknowledgements
Cities and country lists corresponding to latitude and longitude are
    courtesy of https://simplemaps.com/data/world-cities.

Eyring, V., Bony, S., Meehl, G. A., Senior, C. A., Stevens, B., Stouffer, R. J.,
    and Taylor, K. E.: Overview of the Coupled Model Intercomparison Project
    Phase 6 (CMIP6) experimental design and organization, Geosci. Model Dev., 9,
    1937–1958, https://doi.org/10.5194/gmd-9-1937-2016, 2016.

## Licensing
MIT License

Copyright (c) 2019 NCAR CMIP6 Hackathon

*See LICENSE document [here](LICENSE)*
