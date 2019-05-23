import json
import requests
import collections

SERVER = 'https://tokyo.sdelements.com'
API_TOKEN = 'f258c47557a3f98f55d4fbd0cb9d8354c86fbb52'
PROJECTS_URL = '{server}/api/v2/projects/?page_size=100'.format(server=SERVER)
REQUESTS_HEADER = {
    'Authorization': "Token " + API_TOKEN,   # Authorization header + generated API TOKEN
    'Accept': "application/json"             # Accepts API response in JSON format
}

url = PROJECTS_URL
profiles = []
while True:
    response = requests.get(url, headers=REQUESTS_HEADER) 
    data = response.json()

    for item in data['results']:    # loop through the values in the results key 
        profiles.append(item['profile']['name'])    # add each profile's name to list

    if data["next"]:    # check if a value is present in "next" 
        url = data["next"]
    else:
        break   # leave the infinite loop if your on the last page

for profile, count in collections.Counter(profiles).items():    # count the profile occurences  
    print(u"{} : {}".format(profile, count))
