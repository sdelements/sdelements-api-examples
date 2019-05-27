import json
import requests
import collections

SERVER = 'https://tokyo.sdelements.com'
API_TOKEN = 'f258c47557a3f98f55d4fbd0cb9d8354c86fbb52'
PROJECTS_URL = '{server}/api/v2/projects/?page_size=100'.format(server=SERVER)
REQUESTS_HEADER = {
    # Authorization header + generated API TOKEN
    'Authorization': "Token " + API_TOKEN,
    'Accept': "application/json"             # Accepts API response in JSON format
}
url = PROJECTS_URL
profiles = []

while True:
    response = requests.get(url, headers=REQUESTS_HEADER)
    data = response.json()
# Fetches all the profile names(including duplicates) stored in the API response
    profiles += [project['profile']['name'] for project in data['results']]
# Grab the URL of the next page of results to fetch; if this entry is blank we have reached the last page
    if data["next"]:
        url = data["next"]
    else:
        break
for profile, count in collections.Counter(profiles).items():
# Counts the number of times each profile occurs in the list using Python's collection's module
    print(u"{} : {}".format(profile, count))
