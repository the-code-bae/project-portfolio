#!/usr/bin/env python
# coding: utf-8

import requests
import os
import pandas as pd
# import time
import concurrent.futures
from collections import namedtuple


# TODO Documentation

class TflStopPoint:
    def __init__(self,mode):
        self.mode = mode
        
    @property
    def endpoint(self):
        return f"https://api.tfl.gov.uk/StopPoint/Mode/{self.mode}"
    
    @property
    def stopPoint_json(self):
        try:
            r = requests.get(self.endpoint, timeout = 30)
        except:
            return None
            
        if r.status_code == 200:
            return r.json()
        else:
            return None
    
    @property
    def stopPoint_df(self):
        # dict keys of items to retrieve from json
        desired_keys = [ 'indicator','naptanId', 'stationNaptan', 'lines', 'lineGroup', 'placeType'
                       , 'stopType', 'commonName', 'modes', 'lat', 'lon']

        data=[]
        if self.stopPoint_json != None:
            for i, value in enumerate(self.stopPoint_json['stopPoints']):

                stopPoint = {}

                for key in desired_keys:
                    if key in value:
                        stopPoint[key] = value[key]
                    else:
                        stopPoint[key] = None
                data.append(stopPoint)
        else:
            return None
            
        return pd.DataFrame(data)



tfl_modes = ['dlr', 'national-rail', 'overground', 'tflrail', 'tube']


def get_stopPoint_df(mode):
    return TflStopPoint(mode).stopPoint_df

# TODO currently takes 60 seconds to do, can we optimise?
# Got it down to 30 seconds, can you further reduce that?

# start = time.time()

futures = []
results = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    
    for mode in tfl_modes:
        futures.append(executor.submit(get_stopPoint_df, mode=mode))
        
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

# end = time.time()

# print("Time Taken: {:.6f}s".format(end-start))


# len(results)

# Remove none type from from results
results = [x for x in results if x is not None]


# In[8]:


# len(results)


# In[9]:


df = pd.concat(results, ignore_index=True)


# In[10]:


# Check total df len is equal to that of the individual results
# sum([len(x) for x in results]) == len(df)


# In[11]:


# df.tail()


# In[12]:


# created a named tuple object
# Station = namedtuple('Station', ['name', 'latitude', 'longitude'])


# In[13]:


# TODO create array for use in the finding nearest stations script
LONDON_STATIONS = [Station(s[0], s[1], s[2]) for s in df[['commonName', 'lat', 'lon']].values]


# In[14]:


# check lengths match
# len(LONDON_STATIONS) == len(df)


# In[15]:


# LONDON_STATIONS[0]


# In[16]:


# LONDON_STATIONS[0].name


# In[17]:


# LONDON_STATIONS[0][0]


# In[19]:


# for station in LONDON_STATIONS[:5]:
#     print(station.name)
#     print(station.latitude)
#     print(station.longitude)
#     print('\n')


# In[ ]:




