import os
import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

request_url = "https://cd.sdelements.com/api/v2/users/"

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

request_body = {
    "email": "user@example.com",  # User's email
    "first_name": "Bob",  # First name of the user
    "last_name": "Smith",  # Last name of the user
    "role": "UR5",  # Id of the role to add user to. Not required.
    "groups": ["G1", "G2"]  # Ids of the groups to add user to. Not required.
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the new business unit created from the response, type will be dict
new_user = response.json()
print new_user
