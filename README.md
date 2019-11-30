[![Build Status](https://travis-ci.org/czarakas/local-climate-data-tool.svg?branch=master)](https://travis-ci.org/czarakas/local-climate-data-tool)
[![Coverage Status](https://coveralls.io/repos/github/czarakas/local-climate-data-tool/badge.svg)](https://coveralls.io/github/czarakas/local-climate-data-tool)

# Local Climate Data Tool
This local climate data tool displays the data from CMIP-6 output for historical
and 4 different future scenarios via the Shared Socioeconomic Pathways (SSPs)
described below. The motivation for this tool is to make climate data more
accessible to people with little to no computing knowledge or background in
atmospheric science or climate studies.

### SSPs
Used the Tier 1 - 21st century scenarios listed below ranging from highest to lowest
emission scenarios.

1. SSP5: Fossil-Fueled Development
1. SSP3: Regional Rivalry
1. SSP2: Middle of the Road
1. SSP1: Sustainability

These scenarios are different shared socioeconomic pathways (SSPs), which make projections
on what would happen in the future based on various assumptions of human activity, e.g. how
much carbon-based energy is used and the amount of carbon emissions, assuming no further
climate change or changing policies. In the order of most to least sustainable, these assumptions
are SSP1: Sustainability, SSP2: Middle-of-the-road, SSP3: Regional Rivalry, and SSP5: Fossil
Fueled Development.

*See [here](https://doi.org/10.5194/gmd-9-1937-2016) for a very detailed explanation.*

### Historical
1. Modeled Historical: CMIP6 historical simulation
1. Observed Historical: data from Berkeley Earth Surface Temperatures ([BEST](http://berkeleyearth.org/about-data-set/))

The CMIP6 data has a modeled version of historical data - These models were run for a historical
experiment to recreate the past to validate the models and for several different future scenarios.
These temperature observations come from the Berkeley Earth Surface Temperature (BEST) dataset,
which consists of monthly means of land surface air temperature observations that have been
structured onto a 1° x 1° latitude-longitude grid, although observations may not be available for
every point on the grid at all time steps. For more information, visit
[http://berkeleyearth.org/](http://berkeleyearth.org/).

## User Guide
Install package by cloning this repository then running setup.py in this current directory.

Created by a team of researchers at the University of Washington. For bugs and
    issues, report them [here](https://github.com/czarakas/local-climate-data-tool/issues).

## Directory Hierarchy
This section describes the set up of the directories in this repository.
**Analysis**: comprises all of the python scripts and notebooks to analyze and
            generate the panel application for interactive visualization of
            the data.

1. Examples: contains example code from CMIP6 hackathon
1. Phase1_ProcessData: files to process the data into a format that
   readable for input into the panel application
1. Phase2_CreateApp: files to generate the panel application that
   displays the interactive dash board for user interaction.

**Data**: holds the files containing the data from CMIP6 (scenario models and historical model)
    and BEST (historical reanalysis data).
**environment.yml**: contains dependencies for you to install the environment used for this project.

```            
conda env create -f environment.yml
```
**docs**: contains documentation and documents required for cse583 class project.
1. Functional_Specification.pdf
1. Component_Specification.pdf
1. TechnologyReview.pptx

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
