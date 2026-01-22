"""
see -- https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from colorama import Fore, Style
from ott.utils import date_utils
from . import cmdline


class Threads():
    lock = threading.Lock()
    exit_flag = threading.Event()
    threads = []
    num_threads = 0

    processing_time = 0
    start_time = 0
    end_time = 0
    avg = 0
    rps = 0
    success = 0
    fail = 0
    empty = 0

    tester_function = None
    setup_function = None
    app_name="stress"
    misc_url = ""

    def __init__(self, app_name="stress", num_threads=0, tester_function=None, setup_function=None):
        self.app_name = app_name
        self.num_threads = num_threads
        if tester_function:
            self.tester_function = tester_function
        if setup_function:
            self.setup_function = setup_function

    def set_threads(self, t):
        try:
            self.num_threads = int(t)
        except:
            self.num_threads = 1

    def runner(self):
        while not self.exit_flag.is_set():
            with self.lock:
                if self.setup_function:
                    self.setup_function()

            print(".", end="", flush=True)
            response = False
            if self.tester_function:
                response = self.tester_function()
            if response:
                with self.lock:
                    self.success+=1
            else:
                with self.lock:
                    self.fail+=1

    def run(self):
        # if needed, prompt the user for the number of threads
        if self.num_threads is None or self.num_threads < 1:
            self.num_threads = int(input("Enter the number of threads to use: "))

        cmdline.make_cmd_line(f"poetry run {self.app_name}")

        # create/start the threads
        self.start_time = time.time()
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.runner)
            t.start()
            self.threads.append(t)
        try:
            # Keep the main thread alive until interrupted
            while True:
                pass
        except KeyboardInterrupt:
            print("\nInterrupt signal received. Stopping the load testing...")
            self.exit_flag.set()

            # wait for threads to finish
            for t in self.threads:
                t.join()

            self.end_time = time.time()
            if self.success or self.fail:
                self.avg = self.processing_time / (self.success + self.fail)
            self.processing_time = self.end_time - self.start_time
            self.rps = (self.success + self.fail) / self.processing_time
            self.tm = date_utils.format_seconds(self.processing_time)

    def get(self, url):
        response = requests.get(url)

        with self.lock:
            #print(url); print(response.text[-50:-2])
            #import pdb; pdb.set_trace()
            self.misc_url = url
            mark = "."

            if len(response.text) < 10:
                mark = "_"
                self.empty += 1
                #print(url)

            if response.status_code == 200:
                self.success += 1
            else:
                self.fail += 1

            print(mark, end="", flush=True)

    def get_json(self, url, element=None):
        response = requests.get(url)

        with self.lock:
            #import pdb; pdb.set_trace()
            self.misc_url = url
            mark = "."

            if response.status_code == 200:
                json = response.json()
                if json is None:
                    self.fail += 1
                else:
                    self.success += 1
                    if element:
                        el = json.get(element)
                        if el is None or len(el) < 1:
                            mark = "_"
                            self.empty += 1
            else:
                self.fail += 1

            print(mark, end="", flush=True)


    def print(self):
        print(f"\n\n\n\n*******************************************************\n*\n"
              f"*   \033[1;4m{self.misc_url}\033[0m\n" 
              f"*   {Style.BRIGHT}{self.num_threads}{Style.RESET_ALL} different 'users' (threads)\n" 
              f"*   {Style.BRIGHT}{self.tm}{Style.RESET_ALL} running time\n"
              f"*   {Fore.GREEN}{self.success} successful requests {Fore.RED}(fails {self.fail}){Style.RESET_ALL} (empty response {self.empty})\n"
              f"*   {self.avg:.2f} secs per request (on average)\n"
              f"*   {round(self.rps)} requests per second\n"
              "*\n*******************************************************\n\n"
        )

def main():
    def default(thread=None):
        time.sleep(1)
        return True

    def pre_tester():
        pass

    t = Threads(tester_function=default, setup_function=pre_tester)
    t.run()
    t.print()
