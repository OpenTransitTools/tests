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


def make_requests():
    from .test_suite import TestSuiteList
    l = TestSuiteList.factory()
    return l.get_requests()

