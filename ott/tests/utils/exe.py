"""
run otp via trip plans defined in ./templates/*.mako
"""
import requests


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

    if coords == None:
        from ..test_suite import TestSuiteList
        l = TestSuiteList.factory()
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