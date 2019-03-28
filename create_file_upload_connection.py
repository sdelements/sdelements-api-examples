import os
import requests  # Excellent library for making HTTP requests with python

# Set the API token, here I get it from an environment variable
API_TOKEN = os.environ['SDE_API_TOKEN']


request_url = "https://cd.sdelements.com/api/v2/jobs/analysis-file/"

file_path = "./test.xml"
file_type = "text/xml"

upload_file = {'report_file': ('report.xml', open(file_path, 'rb'), file_type)}

request_headers = {
    # All SDE API requests need an Authorization header with API token
    'Authorization': "Token " + API_TOKEN,
}

request_body = {
    "project": "10",  # The ID of the project the FileUpload belongs to
    # Type of FileUpload you would like to initiate
    "system": "webinspect_file_upload"
}

# Send the HTTP request to the API
response = requests.post(request_url, files=upload_file,
                         headers=request_headers, data=request_body)

if not response.ok:
    # Request did not go through because of an error, print the error
    print "{r.status_code} {r.reason}: {r.text}".format(r=response)
    exit()

# Print the response received from the server
print(response.content)
