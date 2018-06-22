import os
import re
import requests

from defusedxml import minidom

SDE_SERVER = os.environ['SDE_SERVER'] # The server, for example: cd.sdelements.com
API_TOKEN  = os.environ['SDE_API_TOKEN']  # Set the API token, here I get it from an environment variable
PROJECT_ID = os.environ['SDE_PROJECT_ID'] # The project ID. You can get it on the overview page as of v4.15.

request_headers = {
    'Authorization': "Token " + API_TOKEN,  # All SDE API requests need an Authorization header with API token
    'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
    'Accept': "application/json",  # Ask the API to send the response in JSON
}

test_file = "results.xml" # The report file is hard-coded here, you may want to make it a parameter

try:
    base = minidom.parse(test_file)
except Exception as err:
    raise Error("Error opening report xml (%s): %s" % (test_file, str(err)))

for test in base.getElementsByTagName('testcase'):
    match = re.search('SDE\_([^\_]+)\_(low|high)', test.attributes['name'].value)
    if match:

        task_id = match.groups(0)[0]
        confidence = match.groups(0)[1]

        findings = []

        if test.attributes['status'].value == 'passed':
            if confidence == 'low':
                verification_status = 'partial'
            else:
                verification_status = 'pass'
        else:
            verification_status = 'fail'
            findings.append({
                'count': 1,
                'desc': test.attributes['name'].value
            })

        request_url = "https://{server}/api/v2/projects/{project_id}/tasks/{task_id}/analysis-notes/".format(server=SDE_SERVER,project_id=PROJECT_ID, task_id="{0}-{1}".format(PROJECT_ID, task_id))

        request_body = {
            'confidence': confidence,
            'finding_ref': test_file,
            'status': verification_status,
            'behaviour': 'replace', # change if you wish
            'findings': findings
        }

        response = requests.post(request_url, json=request_body, headers=request_headers)

        if response.ok:
            print "{0} updated with verification {1} having {2} confidence".format(task_id, verification_status, confidence)
