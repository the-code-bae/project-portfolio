import api_token
import todoist as td

api = td.TodoistAPI(api_token.token)
api.sync()

# get full name
full_name = api.state['user']['full_name']
# print(full_name)

# view structure
# print(api.state['projects'][0])

# print(api.state['labels'])

# # print names of all projects
# for project in api.state['projects']:
#     print(project['name'])
#     print(project['id'])
#
# # check type of state
# # print(type(api.state['projects'][0]))

# get all completed tasks since a given day
print(api.completed.get_all(since ='2020-12-29T00:00'))
for d in api.completed.get_all(since ='2020-12-29T00:00')["projects"]:
    print(d)
    # print(d['name'])
