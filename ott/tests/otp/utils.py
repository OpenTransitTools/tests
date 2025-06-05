"""
utils for this project
"""
import os
import inspect
from ott.utils.parse.cmdline import base_cmdline

import logging
log = logging.getLogger(__file__)


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


def add_cmd_line_util_args(parser):
    """add util cmd line args"""
    #import pdb; pdb.set_trace()
    parser.add_argument(
        '--url',
        '-u',
        required=False,
        default=None,
        help=f"graphql ws url ala {url}"
    )

    parser.add_argument(
        '--threads',
        '-t',
        required=False,
        default=0,
        help="how many threads to start up"
    )

    ret_val = parser.parse_args()
    set_url(ret_val.url)
    set_threads(ret_val.threads)

    return ret_val


def make_cmd_line(app=""):
    """create and process the cmdline processor"""
    parser = base_cmdline.empty_parser("poetry run " + app)
    ret_val = add_cmd_line_util_args(parser)
    return ret_val


def parse_place(pre, place):
    """ 
    break up any PLACE::45.5,-122.5 into name, lat, lon parts
    """
    ret_val = {}
    try:
        name = lat = lon = None
        parts = place.split("::")
        ll = parts[0]
        if len(parts) == 2:
            name = parts[0]
            ll = parts[1]
        ll = ll.split(",")
        lat = ll[0]
        lon = ll[1]
        ret_val = {pre + 'name': name, pre + 'lat': lat, pre + 'lon': lon}
    except Exception as ex:
        log.warning(ex)
    return ret_val


def main():
    make_cmd_line("util")
    print(url)
    print(threads)
