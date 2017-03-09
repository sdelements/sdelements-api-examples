import os

import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

project_id = 1936  # The id of the project this task belongs to
task_id = "1936-T2"  # The id of the task to modify
request_url = "https://cd.sdelements.com/api/v2/projects/{project_id}/tasks/{task_id}/".format(project_id=project_id,
                                                                                               task_id=task_id)

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

request_body = {
    "status": "TS1"  # New status
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the updated task from the response, type will be dict
task = response.json()
print task
