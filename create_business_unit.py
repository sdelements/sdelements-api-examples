import os
import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

request_url = "https://cd.sdelements.com/api/v2/business-units/"

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

request_body = {
    "name": "Test Business Unit",  # The name of the new business unit.

    # A list of dictionaries representing the users who are part of the business unit.
    # Each dictionary has an email field.
    # This field is not required
    "users": [
        {'email': "test@example.com"},
        {'email': "test2@example.com"},
    ],

    # A list of dictionaries representing the groups which are part of the business unit.
    # Each dictionary has an id field which is the group id.
    # This field is not required
    "groups": [{"id": "G1"}, {"id": "G2"}],

    # A list of dictionaries representing the default user roles for the users in the business unit.
    # Each dictionary has an email field and a role field where the role is the role id.
    # The users specified here should be members of the business unit unless all_users is true.
    # This field is not required
    "default_users": [{"email": "test@example.com", "role": "PR4"}],

    # A list of dictionaries representing the default group roles for the users in the business unit.
    # Each dictionary has an id field which is the group id and a role field where the role is the role id.
    # The groups specified here should be members of the business unit unless all_users is true.
    # This field is not required
    "default_groups": [{"id": "G1", "role": "PR4"}],

    # Whether the business unit includes all users.
    # Trying to create a business unit with this field set to True and specific users/groups specified is an error.
    # Default is false. This field is not required.
    "all_users": False,
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the new business unit created from the response, type will be dict
new_business_unit = response.json()
print new_business_unit
