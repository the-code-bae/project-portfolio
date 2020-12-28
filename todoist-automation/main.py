import api_token
import todoist as td

api = td.TodoistAPI(api_token.token)
api.sync()

# get full name
full_name = api.state['user']['full_name']
print(full_name)

# view structure
print(api.state['projects'])

# print names of all projects
for project in api.state['projects']:
    print(project['name'])

# check type of state
print(type(api.state['projects'][0]))
