from __future__ import print_function
import sys
import os
import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable
SDE_HOST = os.environ['SDE_HOST'] or 'cd.sdelements.com'

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

def get_projects():
    project_ids = []
    request_url = "https://{0}/api/v2/projects/?page_size=100".format(SDE_HOST)

    while True:
        # Send the HTTP request to the API
        response = requests.get(request_url, headers=request_headers)

        if not response.ok:
            # Request did not go through because of an error, print the error
            raise Exception("{r.status_code} {r.reason}: {r.text}".format(r=response))

        for project in response.json()['results']:
            project_ids.append(project['id'])

        if response.json()['next']:
            request_url = response.json()['next']
        else:
            break

    return project_ids

def accept_updates(project_id):
    request_url = "https://{0}/api/v2/projects/{1}/task-updates/".format(SDE_HOST, project_id)
    response = requests.post(request_url, headers=request_headers)
    if not response.ok:
         raise Exception("Could not accept updates for project {0}: {r.status_code} {r.reason}: {r.text}".format(project_id, r=response))

project_ids = get_projects()

print ("{0} projects detected.".format(len(project_ids)))

counter = 0

for project_id in project_ids:
    counter += 1

    accept_updates(project_id)

    sys.stdout.write("\rApplying content updates: %d%%" % round(counter * 100/len(project_ids), 0))
    sys.stdout.flush()

print ("Completed.")

sys.exit(os.EX_OK)
