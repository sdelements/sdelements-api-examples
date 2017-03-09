import os
import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

request_url = "https://cd.sdelements.com/api/v2/projects/"

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

request_body = {
    "application": 1280,  # The ID of the application the project should be created under.
    "name": "API Test",  # The name of the new project.

    # The ID of the desired profile for the project.
    # This field is not required
    "profile": "P9",

    # A boolean field to lock or unlock the project.
    # It can only be used by users that have lock_project_survey permission
    # This field is not required
    "locked": False
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the new business unit created from the response, type will be dict
new_project = response.json()
print new_project
