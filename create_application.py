import os
import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

request_url = "https://cd.sdelements.com/api/v2/applications/"

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

request_body = {
    "business_unit": 1,  # The ID of the business unit the application belongs to
    "name": "API Test",  # The name of the new application

    # Specifies the priority of the application to be either '0-none', '1-high', '2-medium' or '3-low'
    # This field is not required
    "priority": "0-none"
}

# Send the HTTP request to the API
response = requests.post(request_url, json=request_body, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the new application created from the response, type will be dict
new_application = response.json()
print new_application
