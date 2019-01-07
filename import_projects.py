from string import Template

import argparse
import csv
import json
import os
import re
import requests


def get_headers(args):
    return {
        'Authorization': "Token {0}".format(args.sde_api_token), # All SDE API requests need an Authorization header with API token
        'Content-Type': "application/json",  # Tell the API the format of the data sent is JSON
        'Accept': "application/json",  # Ask the API to send the response in JSON
    }

def transform_value(value, data):

    macros = re.findall('\$\{?([a-zA-Z0-9_]+)\}?', value)
    for macro in macros:
        if macro not in data:
            data[macro] = ''
        if not isinstance(data[macro], basestring):
            return data[macro]

    return Template(value).substitute(data)


def get_or_create_bu(args, bu_name):
    
    # Send the HTTP request to the APIa
    params = {
       'name': bu_name
    }
    request_url = "https://{0}/api/v2/business-units/".format(args.sde_host)
    response = requests.get(request_url, params=params, headers=get_headers(args))

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    # Get the new project created from the response, type will be dict
    results = response.json()['results']

    if results:
        bu = results[0]

    else:
        request_body = {
            "name": bu_name
        }

        # Send the HTTP request to the API
        request_url = "https://{0}/api/v2/business-units/".format(args.sde_host)
        response = requests.post(request_url, json=request_body, headers=get_headers(args))
        if not response.ok:
            # Request did not go through because of an error, print the error
            print "{r.status_code} {r.reason}: {r.text}".format(r=response)
            exit()

        bu = response.json()

    return bu

def get_or_create_application(args, bu_id, app_name, attrs):
    params = {
       'business_unit': bu_id,
       'name': app_name
    }

    # Send the HTTP request to the APIa
    request_url = "https://{0}/api/v2/applications/".format(args.sde_host)
    response = requests.get(request_url, params=params, headers=get_headers(args))

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    # Get the new project created from the response, type will be dict
    results = response.json()['results']

    if results:
        app = results[0]

    else:
        request_body = {
            "business_unit": bu_id,
            "name": app_name,
            "custom_attributes": attrs
        }

        # Send the HTTP request to the API
        request_url = "https://{0}/api/v2/applications/".format(args.sde_host)
        response = requests.post(request_url, json=request_body, headers=get_headers(args))
        if not response.ok:
            # Request did not go through because of an error, print the error
            print "{r.status_code} {r.reason}: {r.text}".format(r=response)
            exit()

        app = response.json()

    return app


def create_project(args, application_id, project_name, profile_id, attrs):
    request_body = {
        "application": application_id,  # The ID of the application the project should be created under.
        "name": project_name,  # The name of the new project.

        # The ID of the desired profile for the project.
        # This field is not required
        "profile": profile_id,
        "custom_attributes": attrs
    }

    # Send the HTTP request to the APIa
    request_url = "https://{0}/api/v2/projects/".format(args.sde_host)
    response = requests.post(request_url, json=request_body, headers=get_headers(args))

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    # Get the new project created from the response, type will be dict
    return response.json()


def import_project(args, row, mapping):

    bu_name = transform_value(mapping['business_unit'], row)
    app_name = transform_value(mapping['application_name'], row)
    project_name = transform_value(mapping['project_name'], row)

    project_attrs = {}
    for a in mapping['project_attrs'].keys():
        project_attrs[a] = transform_value(mapping['project_attrs'][a], row)

    app_attrs = {}
    for a in mapping['application_attrs'].keys():
        app_attrs[a] = transform_value(mapping['application_attrs'][a], row)


    bu = get_or_create_bu(args, bu_name)
    app = get_or_create_application(args, bu['id'], app_name, app_attrs)
    return create_project(args, app['id'], project_name, 'P1', project_attrs)

def main(args):
    count =0 
    start = 0
    length = 0

    if args.row_start and args.length:
        start = int(args.row_start)
        length = int(args.length)

    mapping = {}
    with open(args.mapping) as json_data:
        mapping = json.load(json_data)


    with open(args.csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count += 1

            if args.row_start and args.length:
                if count < start or count >= (start + length):
                    continue

            print "Processing row: {0}".format(count)

            prj = import_project(args, row, mapping)
            print prj['url']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import projects to SD Elements using CSV')
    parser.add_argument('--csv', help='Project source code to scan', required=True)
    parser.add_argument('--mapping', help='Dependency Check report (optional)', required=True)
    parser.add_argument('--row_start', help='Row to start import', required=False)
    parser.add_argument('--length', help='Number of entries to import', required=False)
    parser.add_argument('--sde_host', help="FQDN of SD Elements server", required=True)
    parser.add_argument('--sde_api_token', help="API Token for SD Elements server", required=True)

    args = parser.parse_args()

    main(args)
