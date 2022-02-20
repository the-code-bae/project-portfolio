# Documentation - This script uses the Todoist Sync API: https://developer.todoist.com/sync/v8/#get-all-completed-items

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
YESTERDAY_START = str(YESTERDAY) + "T00:00"
YESTERDAY_END = str(YESTERDAY) + "T23:59"

# TODO create function to make sure date is in the correct format

class TodoistConnector:
    def api_client(self, api_token=None):
        api_token = api_token or TODOIST_API_TOKEN
        return todoist.TodoistAPI(api_token)

    def has_values(self, dictionary):
        # For each key in dictionary, check if keys in dict have values
        bool_values = [any(dictionary[key]) for key in dictionary]

        # Create a unique list of values
        output = list(set(bool_values))
        return output[0]

    def get_completed_tasks(self, limit=None, start=None, end=None):
        # Create API client
        api = self.api_client()

        # Sync to API to get latest data
        api.sync

        completed_tasks_data = []
        limit = limit or 5
        start = start or YESTERDAY_START
        end = end or YESTERDAY_END
        offset = 0
        is_empty = 0
        api_calls = 0

        while is_empty == 0:

            data = api.completed.get_all(limit=limit
                                         , offset=offset
                                         , since=start
                                         , until=end)

            if self.has_values(data):
                completed_tasks_data.append(data)  # add items to list
                offset += limit  # increase offset to get the next set of results
                logging.info(f'API call: #{api_calls + 1}, list count: {len(data)}, item count: {len(data["items"])}')
                api_calls += 1

            else:
                is_empty += 1
                logging.info(f'Total API calls made: {api_calls}')

        return completed_tasks_data

    def add_project_name(self, item, data):
        # Convert the project id from the item dictionary into a string
        project_id = str(item['project_id'])

        # Create new key value pair including project name
        item['project_name'] = data[project_id]['name']
        return item

    def convert_to_list_of_dicts(self, response_data):
        output = []
        for response in response_data:
            for item in response['items']:
                row = self.add_project_name(item, response['projects'])
                output.append(row)
                print(row)  # TODO delete?
        return output


# convert_to_list_of_dicts(completed_tasks_data)
# Create list of dictionaries for uploading to bigquery

# Convert to json

# Upload to bigquery

if __name__ == '__main__':
    t = TodoistConnector()
    data = t.get_completed_tasks()
    t.convert_to_list_of_dicts(data)
