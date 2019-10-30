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

def fillDataSet():
    modelnames_toplot = []
    for modelname in modelnames:
        source_id = modelname
        dataset_info_subset = dataset_info[dataset_info['source_id']==source_id]
        institution_id = list(set(dataset_info_subset['institution_id']))[0]
        nametag = activity_id+'.'+institution_id+'.'+source_id+'.'+experiment_id+'.'+this_table_id+'.'+this_grid_label
        if nametag in dset_dict:
            print(modelname)
            print(ds.nbytes/1e9)
            thisdata=dset_dict[nametag]
            thisdata=xr.decode_cf(thisdata)
            newtimes = reindex_time(startingtimes = thisdata['time'])
            thisdata['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
        else:
            continue
    return ds,modelnames_toplot

########### Main Workflow
dict_timeSeries = dict()

for scenario in this_experiment_id:
    experiment_id = scenario
    print('---------------'+experiment_id+'---------------')
    
    # read data from all other models into xarray dataset
    [ds,modelnames_toplot] = fillDataSet()
    
     # Convert from K to C
    for modelname in modelnames_toplot:
        ds[modelname]=ds[modelname]-273.15
        

# print memory stuff with this
ipython_vars = ['In', 'Out', 'exit', 'quit', 'get_ipython', 'ipython_vars']
import sys
memlist = sorted([(x, sys.getsizeof(globals().get(x))) for x in dir() if not x.startswith('_') and x not in sys.modules and x not in ipython_vars], key=lambda x: x[1], reverse=True)
print(memlist)