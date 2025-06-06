
##### TODO #####

"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor


threads = 0
def set_threads(t):
    global threads
    try:
        threads = int(t)
    except:
        pass


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
        else:
            with lock:
                fail+=1


def run():
    utils.make_cmd_line("stress")

    # if needed, prompt the user for the number of threads
    if utils.threads is not None and utils.threads > 0:
        num_threads = utils.threads
    else:
        num_threads = int(input("Enter the number of threads to use: "))


    # create/start the threads
    start_time = time.time()
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
        print("\nInterrupt signal received. Stopping the load testing...")
        exit_flag.set()
        # wait for threads to finish
        for thread in threads:
            thread.join()

        processing_time = time.time() - start_time
        avg = processing_time / (success + fail)
        rps = (success + fail) / processing_time


def main():
    run()
