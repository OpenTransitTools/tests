"""
utils for this project
"""
import os
import inspect
from ott.utils.parse.cmdline import base_cmdline

this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


url = "http://maps8.trimet.org/rtp/gtfs/v1"
def set_url(u):
    global url
    if u and len(u) > 2:
        if u.upper() == "PROD" or u.upper() == "MAPS":
            url = "https://maps.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "RTP":
            url = "https://ws.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "STAGE":
            url = "https://ws-st.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "TEST":
            url = "http://maps8.trimet.org/rtp/gtfs/v1"
        else:
            url = u


threads = 0
def set_threads(t):
    global threads
    try:
        threads = int(t)
    except:
        pass


def cmd_line(app="", do_parse=True):
    #import pdb; pdb.set_trace()
    parser = base_cmdline.empty_parser("poetry run " + app)

    parser.add_argument(
        '--url',
        '-u',
        required=False,
        default=None,
        help="graphql ws url ala http://maps8.trimet.org/rtp/gtfs/v1"
    )

    parser.add_argument(
        '--threads',
        '-t',
        required=False,
        default=0,
        help="how many threads to start up"
    )

    if do_parse:
        ret_val = parser.parse_args()
    else:
        ret_val = parser
    return ret_val


def cmd_line_process(app=""):
    "create and process the cmdline processor"
    ret_val = cmd_line(app)
    set_url(ret_val.url)
    set_threads(ret_val.threads)
    return ret_val


def main():
    cmd_line_process("util")
    print(url)
    print(threads)
