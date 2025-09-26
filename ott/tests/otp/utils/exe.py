"""
run otp via trip plans defined in ./templates/*.mako
"""
import requests
from ..templates import template_utils
from .. import test_suite


def call_otp(query, url, headers=None):
    """ """
    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }
    payload = {
        "query": query
    }
    #print(); print(payload); print()
    response = requests.post(url, headers=headers, json=payload)
    return response


def make_requests(templates=None, coords=None):
    """ returns an array of strings, each being a GraphQL request to OTP """
    ret_val = []

    if templates == None:
        templates = template_utils.make_templates()

    if coords == None:
        l = test_suite.ListTestSuites("x", "y")
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