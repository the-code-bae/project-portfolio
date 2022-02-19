# Documentation: https://developer.todoist.com/sync/v8/#get-all-completed-items
# from typing import Optional
# This script uses the Todoist Sync API

from dotenv import load_dotenv
import os
import todoist
import datetime as dt
import logging

load_dotenv()
logger = logging.getLogger('__name__')
logging.basicConfig(format='[%(asctime)s.%(msecs)03d] %(filename)s - [%(levelname)s] %(message)s'
                    , datefmt='%d-%b-%y %H:%M:%S'
                    , level=logging.INFO)

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# Create yesterday's date variables
TODAY = dt.date.today()
YESTERDAY = TODAY - dt.timedelta(days=1)
YESTERDAY_START = str(YESTERDAY) + "T00:00:00Z"
YESTERDAY_END = str(YESTERDAY) + "T23:59:59Z"

# TODO create function to make sure date is in the correct format

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
                                 , since=YESTERDAY_START
                                 , until=YESTERDAY_END)

    logging.info(f'API call: #{api_call + 1}, list count: {len(data)}, item count: {len(data["items"])}')
    api_call += 1

    if has_values(data):
        completed_tasks_data.append(data)  # add items to list
        offset += limit  # increase offset to get the next set of results
    else:
        is_empty += 1

for line in completed_tasks_data:
    print(line)


def add_project_name(item, data):
    project_id = str(item['project_id'])
    # print(project_id)
    item['project_name'] = data[project_id]['name']
    return item


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

# Upload to bigquery
