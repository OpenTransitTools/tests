"""
basic performance testing
"""
import time
from colorama import Fore, Style
from . import exe


def time_otp_requests():
    """
    show timing stats for each call
    """
    for i, r in enumerate(exe.make_requests()):
        start_time = time.time()
        response = exe.call_otp(r)
        processing_time = time.time() - start_time
        if response.status_code == 200:
            #print(response.json())
            print(f"query #{i:3} {Fore.GREEN}pass: ", end="")
        else:
            #print(response.text())
            print(f"query #{i:3} {Fore.RED}fail: ", end="")
        print(f"{processing_time:.02f}{Style.RESET_ALL} seconds")


def main():
    time_otp_requests()