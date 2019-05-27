import collections
import os

import requests


SERVER = os.environ['SDE_SERVER']         # e.g. https://cd.sdelements.com
API_TOKEN = os.environ['SDE_API_TOKEN']   # e.g. f258c47557a3f98f55d4fbd0cb9d8354c86fbb52

PROJECTS_URL = '{server}/api/v2/projects/?page_size=100'.format(server=SERVER)
REQUESTS_HEADER = {
    'Authorization': "Token " + API_TOKEN,  # Authorization header + generated API TOKEN
    'Accept': "application/json"
}

url = PROJECTS_URL
profiles = []
while True:
    response = requests.get(url, headers=REQUESTS_HEADER)
    data = response.json()
    
    # Extract all the profile names stored in the API response
    profiles += [project['profile']['name'] for project in data['results']]
    
    # Grab the URL of the next page of results to fetch; if this entry is 
    # blank we have reached the last page
    if data["next"]:
        url = data["next"]
    else:
        break

# Count the number of profiles we previously found via the API.
for profile, count in collections.Counter(profiles).items():
    print(u"{} : {}".format(profile, count))