import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from gql import graphql_queries
import random
import os

url = "<URL HERE>"

headers = {
    "Content-Type": "application/json",
    "Authorization": "<token HERE>"
    # Add any additional headers as needed
}

lock = threading.Lock()
exit_flag = threading.Event()
success_counter = 0

def execute_query(query):
    global success_counter
    payload = {
        # use this payload if query is going a query
        # "query": query
        
        # simple send the query as in request.py file
        query
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with lock:
            success_counter += 1
        print(f"{Fore.GREEN}GraphQL query executed successfully:{Style.RESET_ALL}")
        print(response.json())
    else:
        print(f"{Fore.RED}GraphQL query failed with status code: {response.status_code}{Style.RESET_ALL}")
        print(response.text)

def run_query():
    while not exit_flag.is_set():
        with lock:
            query = random.choice(graphql_queries)
        execute_query(query)

def main():
    print(f"{Fore.CYAN}Threaded GraphQL Load Testing Script{Style.RESET_ALL}")
    print("Created by Rahul Kumar")

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

        print(f"{Fore.GREEN}Successful requests: {success_counter}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
