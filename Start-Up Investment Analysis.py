#!/usr/bin/env python
# coding: utf-8

# The following is an exploratory data analysis of real-world data from start-up companies which have received investment, either privately alone, or also with public offerings. We will explore the kinds of sectors these companies work in, and analysis the best/worst sectors for a start-up.

# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')

import sys

np.set_printoptions(threshold=sys.maxsize)
pd.set_option('display.max_columns',999)
pd.set_option('display.max_rows',999)


# In[6]:


df = pd.read_csv("investments2.csv", encoding = "ISO-8859-1", engine='python')
df.head()
# we have information on name, url, category, market, acquired/operating/closed status, and geographical location.


# In[7]:


df['status'].value_counts()
# most of our start-ups are still operating. We will try to see which markets have the most start-ups which have been acquired, 
# vs the markets where the most start-ups have closed.


# In[8]:


df1 = df.drop(['name','homepage_url'], axis = 1)
# name and url can be dropped, they tell us nothing.

df1.iloc[4].isnull().sum() # checks how many NA values in an observation


# In[9]:


df1['funding_total_usd'] = df1['funding_total_usd'].apply(lambda x: str(x).replace(',',''))
# Funding has been encoded with commas - here we remove them.


# Let's take a look at the kinds of markets that these start-ups are operating in, as well as the Operating/Acquired/Closed in these markets.

# In[11]:


dfa = df1[df1['status'] == 'acquired']     # subset 'acquired'
dfo = df1[df1['status'] == 'operating']    # subset 'operating'
dfc = df1[df1['status'] == 'closed']       # subset 'closed'

do = pd.DataFrame(data = dfo['market'].value_counts())  # dataframe of 'operating', value count of markets
do.columns = ['Operating']

da = pd.DataFrame(data = dfa['market'].value_counts())  # dataframe of 'acquired', value count of markets
da.columns = ['Acquired']

dc = pd.DataFrame(data = dfc['market'].value_counts())  # dataframe of 'closed', value count of markets
dc.columns = ['Closed']

dm = pd.DataFrame(data = df['market'].value_counts())  # dataframe of total markets
dm.columns = ['Total']

ds = pd.concat([do,da,dc,dm], axis = 1)

ds


# Let's restrict ourselves to markets where we have at least 60 start-ups.

# In[12]:


ds_short = ds[ds['Total'] > 60]

ds_short


# In[14]:


len(ds_short)


# We are left with 90 markets, each of which has at least 60 instances of a start-up. This is workable.
# 
# To be certain about our numbers, we'll do some calculations to see if we're missing a lot of data.

# In[16]:


oac_sum = pd.DataFrame(data = ds_short.drop(['Total'], axis = 1).sum(axis = 1))  # drop Total
oac_sum.columns = ['Added']  # add columns across

together = pd.concat([ds_short, oac_sum], axis = 1)

together['Missing'] = together['Total'] - together['Added']  # how many missing?
together['Missing_Perc'] = round(together['Missing'] / together['Total'],2)  # to get percentage

together


# We see that for most markets, we are missing only a small percentage of data. This shouldn't cause us any problems.

# Next, let's have a look at Operating/Acquired/Closed by percentage.

# In[18]:


# new columns of percentages

together['Operating_Perc'] = round(together['Operating'] / together['Added'],2) 
together['Acquired_Perc'] = round(together['Acquired'] / together['Added'],2)
together['Closed_Perc'] = round(together['Closed'] / together['Added'],2)


# Below is a list of the top 20 markets with the highest percentage of start-ups still operating.

# In[19]:


together['Operating_Perc'].sort_values(ascending = False).head(20)


# Below is a list of the top 20 markets with the highest percentage of start-ups which have been acquired.

# In[21]:


together['Acquired_Perc'].sort_values(ascending = False).head(20)


# And finally, below is a list of the top 20 markets with the highest percentage of start-ups which have closed.

# In[23]:


together['Closed_Perc'].sort_values(ascending = False).head(20)


# In[ ]:





# So we can see that, from a start-up point of view, there are certain sectors in which it is better to start your business in, both in terms of maintaining business and in being acquired, and similarly, there are certain sectors in which the chances of the business closing down are significantly higher than in others.

# In[ ]:





# 

# In[ ]:




