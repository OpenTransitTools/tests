"""
basic performance testing
"""
import time
from colorama import Fore, Style
from ott.utils import num_utils
from .utils import exe
from .utils import misc
from .utils import cmdline


def time_otp_requests():
    """
    show timing stats for each call
    """
    #import pdb; pdb.set_trace()
    cmdline.make_cmd_line("perf")
    runs = num_utils.to_int_min(misc.threads, 1)

    print(f"{Fore.YELLOW}\033[1;4m{misc.graphql_url}\033[0m {Style.BRIGHT}{Fore.WHITE}Performance Test{Style.RESET_ALL}")
    for z in range(runs):
        for i, r in enumerate(exe.make_requests()):
            start_time = time.time()
            response = exe.call_otp(r, misc.graphql_url)
            processing_time = time.time() - start_time
            if response.status_code == 200:
                #print(response.json())
                print(f"query #{i:3} {Fore.GREEN}pass: ", end="")
            else:
                #print(response.text())
                print(f"query #{i:3} {Fore.RED}fail: ", end="")
            print(f"{processing_time:.02f}{Style.RESET_ALL} seconds")


def main():
    try:
        time_otp_requests()
    except KeyboardInterrupt:
        pass
