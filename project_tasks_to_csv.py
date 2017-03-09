import csv
import os

import requests  # Excellent library for making HTTP requests with python

API_TOKEN = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable

project_id = 1156  # The id of the Project
request_url = "https://cd.sdelements.com/api/v2/projects/{project_id}/tasks/".format(project_id=project_id)

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

# Send the HTTP request to the API
response = requests.get(request_url, headers=request_headers)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Get the new business unit created from the response, type will be dict
tasks = response.json()["results"]

# Headers of the CSV file
csv_headers_row = ["id", "task_id", "url", "title", "text", "priority", "phase", "ad_hoc", "relevant", "accepted",
                   "assigned_to", "updated", "library_task_created", "library_task_updated", "verification_status",
                   "status", "note_count", "artifact_proxy"]

# Create a 2D list of tasks and their attributes to be written into the CSV file
tasks_rows = [[task[header] for header in csv_headers_row] for task in tasks]

# Create the CSV file
with open('./tasks.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers_row)
    writer.writerows(tasks_rows)
