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
    response = requests.get(projects_url, headers=REQUESTS_HEADER)
    response.raise_for_status()

    data = response.json()

    # Extract all the profile names stored in the API response
    for project_id in [project['id'] for project in data['results']]:
        tasks_url = f'{SERVER}/api/v2/projects/{project_id}/task-updates/'
        response = requests.post(tasks_url)
        response.raise_for_status()

    # Grab the URL of the next page of results to fetch; if this entry is
    # blank we have reached the last page
    if data["next"]:
        projects_url = data["next"]
    else:
        break
