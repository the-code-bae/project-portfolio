# Documentation: https://developer.todoist.com/sync/v8/#get-all-completed-items
from dotenv import load_dotenv
import os
import todoist as td
import pandas as pd
import datetime as dt

load_dotenv()

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# # Get yesterday's date to feed into call
# today = dt.date.today()
# yesterday = today - dt.timedelta(days = 1)
# yday_start = str(yesterday)+"T00:00:00Z"
# yday_end = str(yesterday)+"T23:59:59Z"
# print(yday_start)
# print(yday_end)
#
api = td.TodoistAPI(TODOIST_API_TOKEN)
# Sync to API to get latest data
api.sync();

print(api.state['projects'])