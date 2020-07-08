import collections
import os

import requests


SERVER = os.environ['SDE_SERVER']         # e.g. https://cd.sdelements.com
API_TOKEN = os.environ['SDE_API_TOKEN']   # e.g. f258c47557a3f98f55d4fbd0icb9d8354c86fbb52

PROJECTS_URL = f'{SERVER}/api/v2/projects/?page_size=100'

REQUESTS_HEADER = {
    'Authorization': "Token " + API_TOKEN,  # Authorization header + generated API TOKEN
    'Accept': "application/json"
}

print("Fetching projects from: {}".format(PROJECTS_URL))
print("Using API Token: {}...".format(API_TOKEN[:5]))

projects_url = PROJECTS_URL
while True:
    response = requests.get(projects_url, headers=REQUESTS_HEADER, verify=False)
    response.raise_for_status()

    data = response.json()

    # loop over the projects to accept tasks
    for project_id, name in [(project['id'], project['name']) for project in data['results']]:
        tasks_url = f'{SERVER}/api/v2/projects/{project_id}/task-updates/'
        response = requests.get(tasks_url, headers=REQUESTS_HEADER, verify=False)
        response.raise_for_status()

        data = response.json()

        if not data["results"]:
            print(f'Project {name} ({project_id}): no updates')
        else:
            added_tasks = 0
            removed_tasks = 0
            for task in data["results"]:
                if task["accepted"] and not task["relevant"]:
                    removed_tasks += 1
                elif not task["accepted"] and task["relevant"]:
                    added_tasks += 1
            print(f'Project {name} ({project_id}): there are {added_tasks} new tasks and {removed_tasks} removed tasks')

    # Grab the URL of the next page of results to fetch; if this entry is
    # blank we have reached the last page
    if "next" in data:
        projects_url = data["next"]
    else:
        break
