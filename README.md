# Local Climate Data Tool
This local climate data tool displays the data from CMIP-6 output for historical
and 4 different future scenarios via the Shared Socioeconomic Pathways (SSPs)
described below. The motivation for this tool is to make climate data more 
accessible to people with little to no computing knowledge or background in 
atmospheric science or climate studies. 

### SSPs
Used the Tier 1 - 21st century scenarios listed below ranging from highest to lowest
emission scenarios.

1. SSP585: highest emission scenario 
1. SSP370: medium to high forcing pathway, takes into account the land use 
           changes and high emissions (esp. of SO2)
1. SSP245: represents regional downscaling, medium forcing
1. SSP126: low emissions, future goals

*See [here](https://doi.org/10.5194/gmd-9-1937-2016) for a more detailed explanation.*
### Historical
1. CMIP6 historical simulation
1. historical data from Berkeley Earth Surface Temperatures ([BEST](http://berkeleyearth.org/about-data-set/))

## User Guide
TODO: how to install software and use it. 

Created by a team of researchers at the University of Washington. For bugs and
    issues, report them [here](https://github.com/czarakas/local-climate-data-tool/issues).

## Folders
This section describes the set up of the directories in this repository.
- **Analysis**: comprises all of the python scripts and notebooks to analyze and
            generate the panel application for interactive visualization of 
            the data.

    1. Examples: contains example code from CMIP6 hackathon
    1. Phase1_ProcessData: files to process the data into a format that
       readable for input into the panel application
    1. Phase2_CreateApp: files to generate the panel application that 
       displays the interactive dash board for user interaction.
                        
- **Data**: holds the files containing the data from CMIP6 and BEST. 
- **environments**: contains .yml files for you to install the environment used for
            this project.
```            
conda env create -f OceanPangeoEnvironment.yml
``` 
- **docs**: contains documentation such as functional and component specification
            and documents required for cse583 class project. 
           

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