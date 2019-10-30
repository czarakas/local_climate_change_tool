######### Create Functions
### Create ds_out reference file

def reindex_time(startingtimes):
    newtimes = startingtimes.values
    for i in range(0,len(startingtimes)):
        yr = int(str(startingtimes.values[i])[0:4])
        mon = int(str(startingtimes.values[i])[5:7])
        day = int(str(startingtimes.values[i])[8:10])
        hr = int(str(startingtimes.values[i])[11:13])
        newdate = cftime.DatetimeProlepticGregorian(yr,mon,15)
        newtimes[i]=newdate
    return newtimes

def initializeDataSet(activity_id,experiment_id,modelname):
    dataset_info_subset = dataset_info[dataset_info['source_id']==modelname]
    institution_id = list(set(dataset_info_subset['institution_id']))[0]
    nametag=activity_id+'.'+institution_id+'.'+modelname+'.'+experiment_id+'.'+this_table_id+'.'+this_grid_label
    thisdata=dset_dict[nametag]
    thisdata=xr.decode_cf(thisdata)
    thisdata = thisdata.mean(dim=['member_id'])
    ###### Reformat dates to be Proleptic Gregorian date type
    newtimes = reindex_time(startingtimes = thisdata['time'])
    thistime = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
    thisdata['time'] = thistime
    #thisdata=thisdata.groupby('time.year').mean('time')
    thisdata.load()
    ###### Regrid 
    
    #########################################
    thisval=thisdata[this_variable_id] #.mean(dim=['lat','lon'])
    ds = xr.Dataset({modelname: thisval},\
                    coords={'time': thistime})
                            #'modelnames': modelnameInd, \
                            #'lat': thislat, \
                            #'lon': thislon, \
                
    return ds

def fillDataSet():
    modelnames_toplot = []
    for modelname in modelnames:
        source_id = modelname
        dataset_info_subset = dataset_info[dataset_info['source_id']==source_id]
        institution_id = list(set(dataset_info_subset['institution_id']))[0]
        nametag = activity_id+'.'+institution_id+'.'+source_id+'.'+experiment_id+'.'+this_table_id+'.'+this_grid_label
        if nametag in dset_dict:
            
            ######### A BUNCH OF EXCEPTIONS WHERE THINGS BREAK ###############
            if (modelname=='MCM-UA-1-0'):
                # ERROR Different names for lat and lon
                print('** Skipping '+modelname)
            elif (experiment_id=='historical')and(modelname=='CESM2'):
                #ValueError
                print('** Skipping '+modelname)
            elif (experiment_id=='ssp126')and(modelname=='CanESM5'):
                #OutOfBoundsDatetime
                print('** Skipping '+modelname)
            elif (experiment_id=='ssp370')and(modelname=='CESM2-WACCM'):
                #ValueErrorvalues
                print('** Skipping '+modelname)
            elif (experiment_id=='ssp245')and ((modelname=='CAMS-CSM1-0')or (modelname=='HadGEM3-GC31-LL')):
                print('** Skipping '+modelname)
            elif (experiment_id=='ssp585')and((modelname=='CAMS-CSM1-0')or(modelname=='CanESM5')):
                print('** Skipping '+modelname)
            
            ###### Reformat dates to be Proleptic Gregorian date type
            else:
                print(modelname)
                print(ds.nbytes/1e9)
                modelnames_toplot.append(modelname)
                thisdata=dset_dict[nametag]
                thisdata=xr.decode_cf(thisdata)
                thisdata = thisdata.mean(dim=['member_id'])
                newtimes = reindex_time(startingtimes = thisdata['time'])
                thisdata['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
                ###### Regrid this
                thisdata=RegridModel(thisdata)
                #thisdata=thisdata.groupby('time.year').mean('time')
                thisdata.load() #if this is commented out, lazily loading and will be dask function call
                thisval=thisdata[this_variable_id] #.mean(dim=['lat','lon'])
                ds[modelname]=thisval
        else:
            continue
    return ds,modelnames_toplot

########### Main Workflow
dict_timeSeries = dict()

for scenario in this_experiment_id:
    experiment_id = scenario
    print('---------------'+experiment_id+'---------------')
    if experiment_id=='historical':
        activity_id='CMIP'
    else:
        activity_id='ScenarioMIP'
    ds= initializeDataSet(activity_id,experiment_id,modelname='CAMS-CSM1-0')
    
    # read data from all other models into xarray dataset
    [ds,modelnames_toplot] = fillDataSet()
    
     # Convert from K to C
    for modelname in modelnames_toplot:
        ds[modelname]=ds[modelname]-273.15

    #Add dataset to dictionary
    dict_timeSeries[experiment_id] = ds
    dict_timeSeries[experiment_id+'_modelnameToPlot'] = modelnames_toplot
    
    #save ds
    with open(output_path+'timeSeries_byModel_'+scenario+'.pickle', 'wb') as handle:
        pickle.dump(ds, handle, protocol=pickle.HIGHEST_PROTOCOL)