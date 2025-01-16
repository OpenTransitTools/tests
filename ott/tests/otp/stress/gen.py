"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""

import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
import random


url = "https://maps.trimet.org/rtp/gtfs/v1"

headers = {
    "Content-Type": "application/json",
}

graphql_queries = [
    "query GtfsExampleQuery { routes {shortName gtfsId}}"
 ]

lock = threading.Lock()
exit_flag = threading.Event()


def execute_query(query):
    payload = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"{Fore.GREEN}GraphQL query executed successfully:{Style.RESET_ALL}")
        print(response.json())
    else:
        print(f"{Fore.RED}GraphQL query failed with status code: {response.status_code}{Style.RESET_ALL}")
        print(response.text)


def run_query():
    while not exit_flag.is_set():
        with lock:
            query = random.choice(graphql_queries)
        #import pdb; pdb.set_trace()
        execute_query(query)


def main():
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


if __name__ == "__main__":
    main()
