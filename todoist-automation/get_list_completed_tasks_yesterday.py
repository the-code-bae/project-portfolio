# Documentation - This script uses the Todoist Sync API: https://developer.todoist.com/sync/v8/#get-all-completed-items

from dotenv import load_dotenv
import os
import todoist
import datetime as dt
import logging
import json
from google.cloud import bigquery

load_dotenv()
logger = logging.getLogger('__name__')
logging.basicConfig(format='[%(asctime)s.%(msecs)03d] %(filename)s - [%(levelname)s] %(message)s'
                    , datefmt='%d-%b-%y %H:%M:%S'
                    , level=logging.INFO)

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# Create yesterday's date for default
TODAY = dt.date.today()
YESTERDAY = TODAY - dt.timedelta(days=1)


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
        start = (str(start) + "T00:00") or (str(YESTERDAY) + "T00:00")
        end = (str(end) + "T23:59") or (str(YESTERDAY) + "T23:59")
        offset = 0
        is_empty = 0
        api_calls = 0

        while is_empty == 0:

            response_data = api.completed.get_all(limit=limit
                                                  , offset=offset
                                                  , since=start
                                                  , until=end)

            if self.has_values(response_data):
                completed_tasks_data.append(response_data)  # add items to list
                offset += limit  # increase offset to get the next set of results
                logging.info(
                    f'API call: #{api_calls + 1}, list count: {len(response_data)}, item count: {len(response_data["items"])}')
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
        return output

    # TODO Convert to json - to be used to upload to Google Cloud Storage
    def convert_to_json(self, list_of_dicts):
        return json.dumps(list_of_dicts)


# Upload to bigquery
class BigQueryConnector:
    def client(self):
        return bigquery.Client()

    def create_bq_dataset(self, dataset_name):
        client = self.client()

        # Set dataset_id to the ID of the dataset to create.
        dataset_id = f'{client.project}.{dataset_name}'

        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_id)

        # Specify the geographic location where the dataset should reside.
        dataset.location = "EU"

        # Send the dataset to the API for creation, with an explicit timeout.
        dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
        logger.info(f"Created dataset {client.project}.{dataset.dataset_id}")

    def load_single_json_to_bq_table(self, dataset_name, table_name, dict_):
        client = self.client()

        # Set table_id to the ID of the table to create.
        table_id = f"{client.project}.{dataset_name}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, autodetect=True, )

        load_job = client.load_table_from_json(dict_, table_id, job_config=job_config)

        load_job.result()

        destination_table = client.get_table(table_id)
        logger.info(
            f"Loaded {destination_table.num_rows} rows and {len(destination_table.schema)} columns to {table_id}")

    # def load_single_csv_to_bq_table(self, dataset_name, table_name):
    #     client = self.client()
    #
    #     # Set table_id to the ID of the table to create.
    #     table_id = f"{client.project}.{dataset_name}.{table_name}"
    #
    #     job_config = bigquery.LoadJobConfig(
    #         source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True, )
    #
    #     with open(PATH_TO_DIR.joinpath(f'csv/{table_name}.csv'), "rb") as source_file:
    #         job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    #
    #     job.result()
    #
    #     table = client.get_table(table_id)  # Make an API request.
    #     logger.info(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")
    #
    # def load_multiple_csv_to_bq_table(self, dataset_name, table_names_list):
    #     for table in table_names_list:
    #         self.load_single_csv_to_bq_table(dataset_name=dataset_name, table_name=table)


if __name__ == '__main__':
    t = TodoistConnector()
    data = t.get_completed_tasks(start="2022-02-10", end="2022-02-13")
    data_dict = t.convert_to_list_of_dicts(data)

    bqc = BigQueryConnector()
    bqc.load_single_json_to_bq_table('todoist', 'completed_tasks', data_dict)
