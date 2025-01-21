"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""
import os
import json
import inspect
import requests
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from mako.template import Template
from colorama import Fore, Style


this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def call_otp(url, query):
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=payload)
    return response


def main():
    tmpl = Template(filename=os.path.join(this_module_dir, 'templates', 'plan_simple.mako'))
    gql_request = tmpl.render()

    url = "https://maps.trimet.org/rtp/gtfs/v1"
    response = call_otp(url, gql_request)

    if response.status_code == 200:
        print(f"{Fore.GREEN}GraphQL query executed successfully:{Style.RESET_ALL}")
        print(response.json())
    else:
        print(f"{Fore.RED}GraphQL query failed with status code: {response.status_code}{Style.RESET_ALL}")
        print(response.text)

    tmpl = Template(filename=os.path.join(this_module_dir, 'templates', 'plan_connection_complex.mako'))
    gql_request = tmpl.render()
