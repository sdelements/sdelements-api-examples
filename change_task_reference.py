import collections
import os

import requests


SERVER = os.environ['SDE_SERVER']         # e.g. https://cd.sdelements.com
API_TOKEN = os.environ['SDE_API_TOKEN']   # e.g. f258c47557a3f98f55d4fbd0icb9d8354c86fbb52
PROJECT_ID = os.environ['SDE_PROJECT']
TASK_ID = os.environ['SDE_TASK_ID']
REF_ID= os.environ['REF_ID']

REQUESTS_HEADER = {
    'Authorization': "Token " + API_TOKEN,  # Authorization header + generated API TOKEN
    'Accept': "application/json"
}

print("Changing task reference for task: {}-{}".format(PROJECT_ID, TASK_ID))
print("Using API Token: {}...".format(API_TOKEN[:5]))

response = requests.patch(f'https://{SERVER}/api/v2/projects/{PROJECT_ID}/tasks/{PROJECT_ID}-{TASK_ID}/references/{REF_ID}/', data={'reference': 'NEW_REFERENCE'}, headers=REQUESTS_HEADER, verify=False)
response.raise_for_status()

data = response.json()
