"""
run otp via trip plans defined in ./templates/*.mako
"""
import requests
from ..utils import misc

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


def print_request_response(filters, sum):
    """ """
    requests_dict = misc.filter_requests(filters)
    for id, request in requests_dict.items():
        response = call_otp(request)
        print(f"\n\033[1;4mRequest+Response\033[0m #{id}:")
        print(str(request)[4:400]) if sum else print(str(request))
        if response.status_code == 200:
            n = str(response.json())
            print(n[:1000]) if sum else print(n)
        else:
            print(response.text)
        print("\n\n")
