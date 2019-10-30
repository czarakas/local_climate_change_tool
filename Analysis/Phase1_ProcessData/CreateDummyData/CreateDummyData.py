######## Load Packages
import sys

import xarray as xr
import intake
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cftime
import pickle

import util
import DirectoryInfo

######### Create Functions
def reindex_time(startingtimes):
    newtimes = startingtimes.values
    for i in range(0, len(startingtimes)):
        yr = int(str(startingtimes.values[i])[0:4])
        mon = int(str(startingtimes.values[i])[5:7])
        day = int(str(startingtimes.values[i])[8:10])
        hr = int(str(startingtimes.values[i])[11:13])
        newdate = cftime.DatetimeProlepticGregorian(yr, mon, 15)
        newtimes[i] = newdate
    return newtimes

def initializeDataSet(activity_id, experiment_id, modelname):
    dataset_info_subset = dataset_info[dataset_info['source_id'] == modelname]
    institution_id = list(set(dataset_info_subset['institution_id']))[0]
    nametag = activity_id+'.'+institution_id+'.'+modelname+'.'+experiment_id+'.'+this_table_id+'.'+this_grid_label
    thisdata = dset_dict[nametag]
    thisdata = xr.decode_cf(thisdata)
    thisdata = thisdata.mean(dim=['member_id'])
    ###### Reformat dates to be Proleptic Gregorian date type
    newtimes = reindex_time(startingtimes=thisdata['time'])
    thistime = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
    thisdata['time'] = thistime
    #thisdata=thisdata.groupby('time.year').mean('time')
    thisdata.load()
    ###### Regrid 

    #########################################
    thisval = thisdata[this_variable_id] #.mean(dim=['lat','lon'])
    ds = xr.Dataset({'mean': thisval},\
                    coords = {'time': thistime})
                            #'modelnames': modelnameInd, \
                            #'lat': thislat, \
                            #'lon': thislon, \
    return ds

######## Set up workspace
dir_analysis = '/home/jovyan/local-climate-data-tool/Analysis/Phase1_ProcessData'
sys.path.insert(0, dir_analysis)



######### Define Settings for Data Dictionary
this_experiment_id = ['historical', 'ssp126', 'ssp370', 'ssp245', 'ssp585']
this_variable_id = 'tas'
this_table_id = 'Amon'
this_grid_label = 'gn'
output_path = DirectoryInfo.dir_dummyData

######### Create Data Dictionary
import CreateDataDict
[dataset_info, dset_dict, modelnames] = CreateDataDict.createDataDict(this_experiment_id, this_variable_id,
                                                                    this_table_id, this_grid_label)

########### Create files for model data
for scenario in this_experiment_id:
    experiment_id = scenario
    print('-------Creating model data '+experiment_id+'-scenario file-----------')
    if experiment_id == 'historical':
        activity_id = 'CMIP'
    else:
        activity_id = 'ScenarioMIP'
    DS = initializeDataSet(activity_id, experiment_id, modelname='CAMS-CSM1-0')
    DS['min'] = DS['mean']-2
    DS['max'] = DS['mean']+2
    DS['stdev'] = DS['mean']/273

    #save dataset
    with open(output_path+'dummyData_modelData_'+scenario+'.pickle', 'wb') as handle:
        pickle.dump(DS, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #save ds to zarr
    ds.chunk({'lon':10, 'lat':10, 'time':-1})
    ds.to_zarr(output_path+'dummyData_modelData_'+scenario+'.zarr')


########### Create files for "observation" data

experiment_id = 'historical'
print('-------Creating observational data '+experiment_id+' file-----------')
activity_id = 'CMIP'
ds = initializeDataSet(activity_id, experiment_id, modelname='CAMS-CSM1-0')
ds['mean'] = ds['mean'] - 0.5

#save ds to pickle
with open(output_path+'dummyData_observationData'+'.pickle', 'wb') as handle:
    pickle.dump(ds, handle, protocol=pickle.HIGHEST_PROTOCOL)

#save ds to zarr
ds.chunk({'lon':10, 'lat':10, 'time':-1})
ds.to_zarr(output_path+'dummyData_observationData'+'.zarr')