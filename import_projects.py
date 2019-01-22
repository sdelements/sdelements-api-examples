from string import Template

import argparse
import csv
import json
import os
import re
import requests

import logging
import contextlib
try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

debug_requests_on()

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


def get_x_role(args, role_type, role_name, validate_cert):

    params = {}
    request_url = "https://{0}/api/v2/{1}-roles/".format(args.sde_host, role_type)
    response = requests.get(request_url, params=params, headers=get_headers(args), verify=validate_cert)

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    roles = response.json()['results']
    for role in roles:
        if role['name'] == role_name:
            return role['id']

    raise Exception("Missing {0} role: {1}".format(role_type, role_name))

def get_or_create_group(args, group_name, role_name, validate_cert):

    params = {}
    request_url = "https://{0}/api/v2/groups/".format(args.sde_host)
    response = requests.get(request_url, params=params, headers=get_headers(args), verify=validate_cert)

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    groups = response.json()['results']
    for group in groups:
        if group['name'] == group_name:
            return group['id']

    body = {
       'name': group_name,
       'role': get_x_role(args, 'global', role_name, validate_cert)
    }
    response = requests.post(request_url, json=body, headers=get_headers(args), verify=validate_cert)
    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    group = response.json()
    return group['id']

def get_or_create_bu(args, bu_name, groups, validate_cert):

    bu_groups = []
    for g in groups.keys():
        bu_groups.append({
            'id': get_or_create_group(args, g, groups[g], validate_cert),
        })

    # Send the HTTP request to the APIa
    params = {
       'name': bu_name
    }
    request_url = "https://{0}/api/v2/business-units/".format(args.sde_host)
    response = requests.get(request_url, params=params, headers=get_headers(args), verify=validate_cert)

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
            "name": bu_name,
            "groups": bu_groups
        }

        # Send the HTTP request to the API
        request_url = "https://{0}/api/v2/business-units/".format(args.sde_host)
        response = requests.post(request_url, json=request_body, headers=get_headers(args), verify=validate_cert)
        if not response.ok:
            # Request did not go through because of an error, print the error
            print "{r.status_code} {r.reason}: {r.text}".format(r=response)
            exit()

        bu = response.json()

    return bu

def get_or_create_application(args, bu_id, app_name, attrs, validate_cert):
    params = {
       'business_unit': bu_id,
       'name': app_name
    }

    # Send the HTTP request to the APIa
    request_url = "https://{0}/api/v2/applications/".format(args.sde_host)
    response = requests.get(request_url, params=params, headers=get_headers(args), verify=validate_cert)

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
        response = requests.post(request_url, json=request_body, headers=get_headers(args), verify=validate_cert)
        if not response.ok:
            # Request did not go through because of an error, print the error
            print "{r.status_code} {r.reason}: {r.text}".format(r=response)
            exit()

        app = response.json()

    return app


def create_project(args, application_id, project_name, profile_id, groups, attrs, validate_cert):

    proj_groups = []
    for g in groups.keys():
        proj_groups.append({
            'id': get_or_create_group(args, g, "User", validate_cert),
            'role': get_x_role(args, 'project', groups[g], validate_cert)
        })

    request_body = {
        "application": application_id,  # The ID of the application the project should be created under.
        "name": project_name,  # The name of the new project.

        # The ID of the desired profile for the project.
        # This field is not required
        "profile": profile_id,
        "groups": proj_groups,
        "custom_attributes": attrs
    }

    # Send the HTTP request to the APIa
    request_url = "https://{0}/api/v2/projects/".format(args.sde_host)
    response = requests.post(request_url, json=request_body, headers=get_headers(args), verify=validate_cert)

    if not response.ok:
        # Request did not go through because of an error, print the error
        print "{r.status_code} {r.reason}: {r.text}".format(r=response)
        exit()

    # Get the new project created from the response, type will be dict
    return response.json()


def import_project(args, row, mapping, validate_cert):

    bu_name = transform_value(mapping['business_unit']['name'], row)
    app_name = transform_value(mapping['application']['name'], row)
    project_name = transform_value(mapping['project']['name'], row)
    project_profile =  transform_value(mapping['project']['profile'], row)
 
    bu_groups = {}
    for g in mapping['business_unit']['groups']:
        bu_groups[transform_value(g['name'], row)] = transform_value(g['role'], row)

    proj_groups = {}
    for g in mapping['project']['groups']:
        proj_groups[transform_value(g['name'], row)] = transform_value(g['role'], row)

    project_attrs = {}
    for a in mapping['project']['attributes'].keys():
        project_attrs[a] = transform_value(mapping['project']['attributes'][a], row)

    app_attrs = {}
    for a in mapping['application']['attributes'].keys():
        app_attrs[a] = transform_value(mapping['application']['attributes'][a], row)


    bu = get_or_create_bu(args, bu_name, bu_groups, validate_cert)
    app = get_or_create_application(args, bu['id'], app_name, app_attrs, validate_cert)
    return create_project(args, app['id'], project_name, project_profile, proj_groups, project_attrs, validate_cert)

def main(args):
    count =0 
    start = 0
    length = 0
    validate_cert = True

    if args.verify_cert:
        validate_cert = (args.verify_cert.lower() == "true")

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

            prj = import_project(args, row, mapping, validate_cert)
            print prj['url']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import projects to SD Elements using CSV')
    parser.add_argument('--csv', help='Projects to import with other data', required=True)
    parser.add_argument('--mapping', help='Mapping from CSV file to SD Elements', required=True)
    parser.add_argument('--row_start', help='Row to start import', required=False)
    parser.add_argument('--length', help='Number of entries to import', required=False)
    parser.add_argument('--sde_host', help="FQDN of SD Elements server", required=True)
    parser.add_argument('--sde_api_token', help="API Token for SD Elements server", required=True)
    parser.add_argument('--verify_cert', help="Validate TLS server certificates (default=True)", required=False)

    args = parser.parse_args()

    main(args)
