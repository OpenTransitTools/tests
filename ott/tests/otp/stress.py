"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from ott.utils import date_utils
from .utils import exe
from .utils import misc
from .utils import cmdline

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

        response = exe.call_otp(req, misc.url)
        if response.status_code == 200:
            with lock:
                success+=1
            print(f"{Fore.GREEN}.{Style.RESET_ALL}", end="", flush=True)
        else:
            with lock:
                fail+=1
            print(f"{Fore.RED}_{Style.RESET_ALL}", end="", flush=True)


def run():
    cmdline.make_cmd_line("stress")

    # if needed, prompt the user for the number of threads
    if misc.threads is not None and misc.threads > 0:
        num_threads = misc.threads
    else:
        num_threads = int(input("Enter the number of threads to use: "))

    print(f"{Fore.YELLOW}OTP GraphQL Load Test via {misc.url}{Style.RESET_ALL}")

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
        tm = date_utils.format_seconds(processing_time)
        print(f"\n\n\n\n*******************************************************\n*\n"
              f"*   \033[1;4m{misc.url}\033[0m\n" 
              f"*   {Style.BRIGHT}{num_threads}{Style.RESET_ALL} different 'users' (threads)\n" 
              f"*   {Style.BRIGHT}{tm}{Style.RESET_ALL} running time\n"
              f"*   {Fore.GREEN}{success} successful requests {Fore.RED}(fails {fail}){Style.RESET_ALL}\n"
              f"*   {avg:.2f} secs per request (on average)\n"
              f"*   {round(rps)} requests per second\n"
              "*\n*******************************************************\n\n"
        )


def main():
    run()
