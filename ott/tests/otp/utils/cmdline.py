from enum import Enum
import argparse

from ott.utils import date_utils
from ott.utils.parse.cmdline import base_cmdline
from . import misc

import logging
log = logging.getLogger(__file__)


class api(Enum):
    """ see graphql mako templates """
    complex = 'complex'
    simple = 'simple'
    fares = 'fares'
    plan = 'plan'
    tora = 'tora'

    def __str__(self):
        return self.value

    def find_api(self):
        match self:
            case api.complex:
                return "plan_connection_complex.mako"
            case api.fares:
                return "plan_connection_fares.mako"
            case api.plan:
                return "plan_connection_simple.mako"
            case api.simple:
                return "plan_simple.mako"
            case api.tora:
                return "plan_tora.mako"
        return ret_val


class suites(Enum):
    """ see test suite .csv files """
    bike = 'bike'
    bus = 'bus'
    interline = 'interline'
    orange = 'orange'
    upgrade = 'upgrade'
    rail = 'rail'
    regression = 'regression'
    streetcar = 'streetcar'
    walk = 'walk'

    def __str__(self):
        return self.value


def get_args(prog_name='tests', do_parse=True):
    """
    """
    def_url = "maps8.trimet.org"
    
    parser = argparse.ArgumentParser(
        prog=prog_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--url',    '-u',  type=str, default=def_url, help='server to test')
    parser.add_argument('--map_url','-mu', type=str, default=def_url, help='app url link to show itinerary in an app')
    parser.add_argument('--api',    '-a',  type=api, default=api.rest, choices=list(api), help='which OTP api to call')
    parser.add_argument('--suites', '-s',  type=suites, default=None, choices=list(suites), help='csv name of test suite')
    parser.add_argument('--max',    '-m',  type=int, default=3000, help='limit to number of tests')
    parser.add_argument('--stats',  '-stats', '-t', action='store_true', help='print test stats')
    parser.add_argument('--print',  '-print', '-p', action='store_true', help='print test urls')
    parser.add_argument('--curl',   '-curl',  '-c', action='store_true', help='"curl" the url (execute the test)')

    if do_parse:
        args = parser.parse_args()
    else:
        args = parser
    return args


def add_url_arg(parser, parse=False):
    parser.add_argument(
        '--url',
        '-u',
        required=False,
        default=None,
        help=f"graphql ws url ala {misc.url}"
    )
    
    ret_val = None
    if parse:
        ret_val = parser.parse_args()
        misc.set_url(ret_val.url)
    return ret_val
        

def add_cmd_line_util_args(parser):
    """add util cmd line args"""
    add_url_arg(parser)

    parser.add_argument(
        '--threads',
        '-t',
        required=False,
        default=0,
        help="how many threads to start up"
    )

    ret_val = parser.parse_args()
    misc.set_url(ret_val.url)
    misc.set_threads(ret_val.threads)

    return ret_val


def make_cmd_line(app="run_otp"):
    """create and process the cmdline processor"""
    parser = base_cmdline.empty_parser("poetry run " + app)
    parser.add_argument(
        '--filter',
        '-f',
        required=False,
        type=str,
        nargs='+',
        default=['1'],
        help="filter list of trip requests by either string in the request or index of the request list (see poetry run perf_otp) -- example: -f 3 rideHailing 11 22"
    )
    parser.add_argument(
        '--sum',
        '--summarize',
        '-s',
        required=False,
        action="store_true",
        help="summarize results"
    )    
    ret_val = add_cmd_line_util_args(parser)
    return ret_val


def tora_cmdline(app="run_tora"):
    """
    all these cmdline parameters (except for url) are in the plan_tora.mako template. can see the params in action by catting
    the template output.  below is a cmdline that demonstrates all the params being used by said template

    args: poetry run run_tora -fm F -to T -t T -d D -a -m X FLEX -sw SW -avr "XX YY" -b "B" -br BR -bs BS -wr WR -ws WS -cr CR |more
    returns: cmdline (dictionary)
    """
    parser = base_cmdline.empty_parser("poetry run " + app)
    date = date_utils.now_iso_date()
    time = date_utils.now_24_time()
    
    parser.add_argument(
        '-fromPlace', '-fm', type=str, required=False,
        default='PDX::45.5882,-122.5935',
        help='from param (default is PDX::45.5882,-122.5935'
    )
    parser.add_argument(
        '-toPlace', '-to', type=str, required=False,
        default='ZOO::45.5102,-122.7159',
        help='to param (default is ZOO::45.5102,-122.7159)'
    )
    parser.add_argument(
        '-arriveBy', '-a', required=False,
        action="store_true",
        help='arrive by'
    )
    parser.add_argument(
        '-date', '-d', type=str, required=False,
        default=date,
        help=f'date (default is {date})'
    )
    parser.add_argument(
        '-time', '-t', type=str, required=False,
        default=time,
        help=f'time (default is {time})'
    )
    parser.add_argument(
        '-searchWindow', '-sw', type=str, required=False,
        default="4800",
        help='search window (default is 4800 second ... 80 minutes)'
    )
    parser.add_argument(
        '-transportModes', '-tm', '-m', type=str, required=False, nargs='+',
        default=["BUS","TRAM","RAIL","GONDOLA","FLEX"],
        help='modes (default: BUS TRAM RAIL GONDOLA FLEX)'
    )
    parser.add_argument(
        '-allowedVehicleRentalNetworks', '-rent', '-arn', '-avr', '-avrn', type=str, required=False,
        default="",
        help='allowed vehicle rental networks (default: none)'
    )
    parser.add_argument(
        '-banned', '-b', type=str, required=False,
        default="",
        help='banned agencies'
    )
    parser.add_argument(
        '-locale', '-l', type=str, required=False,
        default="en",
        help='language (default is en)'
    )
    parser.add_argument(
        '-walkReluctance', '-wr', type=str, required=False,
        default="11",
        help='walk reluctance (default is 11 - More=3, Normal=11, Less=20)'
    )
    parser.add_argument(
        '-walkSpeed', '-ws', type=str, required=False,
        default="1.34",
        help='walk speed (default is 1.34 mph)'
    )
    parser.add_argument(
        '-bikeReluctance', '-br', type=str, required=False,
        default="7",
        help='bike reluctance (default is 7 - More=3, Normal=7, Less=20)'
    )
    parser.add_argument(
        '-bikeSpeed', '-bs', type=str, required=False,
        default="8.0",
        help='bike speed (default is 8 mph)'
    )
    parser.add_argument(
        '-carReluctance', '-cr', type=str, required=False,
        default="11",
        help='car reluctance (default is 7 - More=3, Normal=11, Less=20)'
    )

    ret_val = add_url_arg(parser, True)
    return ret_val

