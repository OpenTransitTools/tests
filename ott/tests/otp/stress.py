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
from . import exe

lock = threading.Lock()
exit_flag = threading.Event()


def run_query():
    while not exit_flag.is_set():
        with lock:
            query = random.choice(graphql_queries)
        exe.call_otp(query)


def mainX():
    print(f"{Fore.CYAN}Threaded GraphQL Load Testing Script{Style.RESET_ALL}")

    # Prompt the user for the number of threads
    num_threads = int(input("Enter the number of threads to use: "))

    # Create and start the worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=run_query)
        thread.start()
        threads.append(thread)

    try:
        # Keep the main thread alive until interrupted
        while True:
            pass
    except KeyboardInterrupt:
        print("Interrupt signal received. Stopping the load testing...")
        exit_flag.set()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"{Fore.GREEN}Successful requests: {Style.RESET_ALL}")


def main():
    url = "https://maps.trimet.org/rtp/gtfs/v1"
    this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    tmpl = Template(filename=os.path.join(this_module_dir, 'templates', 'plan_simple.mako'))
    gql_request = tmpl.render()

    response = exe.call_otp(url, gql_request)
    if response.status_code == 200:
        print(f"{Fore.GREEN}GraphQL query executed successfully:{Style.RESET_ALL}")
        print(response.json())
    else:
        print(f"{Fore.RED}GraphQL query failed with status code: {response.status_code}{Style.RESET_ALL}")
        print(response.text)



    tmpl = Template(filename=os.path.join(this_module_dir, 'templates', 'plan_connection_complex.mako'))
    gql_request = tmpl.render()
    #print(gql_request)
    #call_otp(gql_request)
