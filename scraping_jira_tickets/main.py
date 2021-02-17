#!/usr/bin/env python
# coding: utf-8

# TODO refactor entire code
# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import re
import os
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import Tk
import datetime as dt


# In[13]:


# print(os.path.dirname(__file__)) wont run in jupyter notebook will run from terminal

directory = os.path.dirname(os.path.abspath(__file__))
todays_date = dt.datetime.today().strftime('%Y_%m_%d_%H%M%S')
# In[2]:


root = Tk()
root.withdraw()
filename = askopenfilename(initialdir = directory)
# Check root is destroyed
root.destroy()


# In[11]:


# print(os.getcwd())


# In[10]:


# print(filename)


# In[3]:


class JiraTickets:
    def __init__(self, file):
        self.file = file
        self._tickets_soup = self._make_soup()
        self._all_tickets = self._get_all_ticket_info()
        self._dict_keys = ['span_class','small_class','title', 'ticket_ref','other','group','status']
        self.tickets_df = self._create_tickets_df()
        self.tickets_count = len(self.tickets_df)
    
    def _make_soup(self):
        return BeautifulSoup(open(self.file), "lxml")
    
    def _get_all_ticket_info(self):
        attr_value_regex = re.compile(r"global-pages.home.ui.tab-container.tab.item-list.item-link#issue-[0-9]{6}")
        all_tickets = self._tickets_soup.find_all(attrs={"data-test-id":attr_value_regex})
        return all_tickets
    
    def _create_ticket_dict(self, x):
    #   Find all span tags  
        data = x.find_all('span')
    #   Flatten list of lists into a single list of string items
        flat_data = [str(item) for sublist in data for item in sublist]
    #   Create dict
        output = dict(zip(self._dict_keys, flat_data))
        return output
    
    def _create_tickets_df(self):    
        dict_output = []
        for x in self._all_tickets:
            dict_output.append(self._create_ticket_dict(x))
        df = pd.DataFrame(dict_output) 
        df['url'] = df.ticket_ref.map('https://justeattakeaway.atlassian.net/browse/{}'.format)
        df['date_script_ran'] = todays_date
        columns = self._dict_keys.copy()
        columns.extend(['url', 'date_script_ran'])
        return df[columns]
    


# In[4]:


my_file = 'jira_your_work.htm'


# In[5]:


x = JiraTickets(filename)


# In[6]:


# x.file


# In[7]:


# x.tickets_df.head()


# In[8]:


print(f"Number of tickets currently open: {x.tickets_count}")


# In[9]:


x.tickets_df.to_csv(os.path.join(directory
                                 , '02_csv'
                                 , todays_date +'jira_tickets.csv'))

