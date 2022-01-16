from dotenv import load_dotenv
import os

load_dotenv()

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
