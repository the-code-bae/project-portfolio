# Documentation: https://developer.todoist.com/sync/v8/#get-all-completed-items
# from typing import Optional
# This script uses the Todoist Sync API

from dotenv import load_dotenv
import os
# import pandas as pd

import todoist
import datetime as dt
import logging

load_dotenv()
logger = logging.getLogger('__name__')
# TODO Change colour of logging message from red to white
logging.basicConfig(format='[%(asctime)s.%(msecs)03d] %(filename)s - [%(levelname)s] %(message)s'
                    , datefmt='%d-%b-%y %H:%M:%S'
                    , level=logging.INFO)

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# Create yesterday's date variables
today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
yesterday_start = str(yesterday) + "T00:00:00Z"
yesterday_end = str(yesterday) + "T23:59:59Z"

api = todoist.TodoistAPI(TODOIST_API_TOKEN)
# Sync to API to get latest data
api.sync()


def has_values(dictionary):
    # For each key in dictionary, check if keys in dict have values
    values = [any(dictionary[key]) for key in dictionary]

    # Create a unique list of values
    output = list(set(values))

    return output[0]


completed_tasks_data = []
limit = 5
offset = 0
is_empty = 0
api_call = 0

while is_empty == 0:

    data = api.completed.get_all(limit=limit
                                 , offset=offset
                                 , since=yesterday_start
                                 , until=yesterday_end)

    logging.info(f'API call: #{api_call + 1}, list count: {len(data)}, item count: {len(data["items"])}')
    api_call += 1

    if has_values(data):
        completed_tasks_data.append(data)  # add items to list
        offset += limit  # increase offset to get the next set of results
    else:
        is_empty += 1

for line in completed_tasks_data:
    print(line)

# TODO Unpack items in lists

completed_tasks_data[0]['items'][0]
completed_tasks_data[0]['items'][0]['project_id']

for i in completed_tasks_data[0]['projects']:
    print(completed_tasks_data[0]['projects'][i])
    print(completed_tasks_data[0]['projects'][i]['name'])


def add_project_name(item, data):
    project_id = str(item['project_id'])
    # print(project_id)
    item['project_name'] = data[project_id]['name']
    return item


add_project_name(completed_tasks_data[0]['items'][0], completed_tasks_data[0]['projects'])


def convert_to_list_of_dicts(response_data):
    output = []
    for response in response_data:
        print(response)
        for j in response['items']:
            print(j)
            row = add_project_name(j, response['projects'])
            output.append(row)
            print(row)
    return output

convert_to_list_of_dicts(completed_tasks_data)
# Create list of dictionaries for uploading to bigquery

# Convert to json
