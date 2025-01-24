"""
run otp via trip plans defined in ./templates/*.mako
"""
import os
import requests
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils
from .test_suite import ListTestSuites
from . import utils


def call_otp(query, headers=None, url=None):
    if url is None:
        url = utils.url
    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }
    payload = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=payload)
    return response


def make_templates():
    ret_val = []
    tmpl_dir=os.path.join(utils.this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(tmpl_dir, ".mako"):
        #print(t)
        tmpl = Template(filename=t, lookup=tl)
        ret_val.append(tmpl)
    return ret_val


def make_requests(templates=None, coords=None):
    """ returns an array of strings, each being a GraphQL request to OTP """
    ret_val = []

    if templates == None:
        templates = make_templates()

    if coords == None:
        l = ListTestSuites("x", "y")
        coords = l.get_latlons()

    for t in templates:
        if coords:
            for c in coords:
                gql = t.render(**c)
                ret_val.append(gql)
        else:
            gql = t.render()
            ret_val.append(gql)

    return ret_val


def filter_requests(filters):
    ret_val = []

    templates = make_templates()
    for f in filters:
        for i, t in enumerate(templates):
            if i == f:
                t = templates[i].render()
                ret_val.append(t)
                break
    return ret_val


def print_request_response(filters, sum=False):
    requests = filter_requests(filters)
    for r in requests:
        response = call_otp(r)
        print(r)
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)
        print("\n\n\n")


def main():
    print_request_response([2, 3])
