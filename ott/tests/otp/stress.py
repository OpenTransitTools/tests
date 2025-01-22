"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from ott.utils import date_utils
from . import exe



lock = threading.Lock()
exit_flag = threading.Event()
success = 0
fail = 0
graphql_requests = exe.make_requests()


def run_query():
    global success
    global fail

    while not exit_flag.is_set():
        with lock:
            req = random.choice(graphql_requests)

        response = exe.call_otp(req)
        if response.status_code == 200:
            with lock:
                success+=1
            print(f"{Fore.GREEN}.{Style.RESET_ALL}", end="", flush=True)
        else:
            with lock:
                fail+=1
            print(f"{Fore.RED}_{Style.RESET_ALL}", end="", flush=True)


def main():
    print(f"{Fore.CYAN}Threaded GraphQL Load Testing Script{Style.RESET_ALL}")

    # Prompt the user for the number of threads
    num_threads = int(input("Enter the number of threads to use: "))
    start_time = time.time()

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

        processing_time = time.time() - start_time
        avg = processing_time / (success + fail)
        tm = date_utils.format_seconds(processing_time)
        print(f"\n{num_threads} different 'users' made {Fore.GREEN}{success} successful requests ({Fore.RED}fails {fail}{Fore.GREEN}) {Style.RESET_ALL}in {Style.BRIGHT}{tm} (avg {avg:.2f}) {Style.RESET_ALL}")
