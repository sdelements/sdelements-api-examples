import os

import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

project_id = 1936  # The id of the Project to update
request_url = "https://cd.sdelements.com/api/v2/projects/{project_id}/".format(project_id=project_id)

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

# All the fields are optional, at least one should be present
request_body = {
    # A boolean field to lock or unlock the project.
    # It can only be used by users that have lock_project_survey permission
    "locked": True,
    "application": 1,  # The ID of the application the project should be under.
    "profile": "P9",  # The ID of the desired profile for the project.
    "archived": False,  # A boolean to archive and unarchive a project.
    "name": "This is the project's new name!",  # The new name of the project.
    "description": "New description!",  # Project description.
    "tags": ["foo", "bar"],  # List of project tags.
    "parent": None,  # Id of the parent project.
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the updated project from the response, type will be dict
project = response.json()
print project
