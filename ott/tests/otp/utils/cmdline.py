from enum import Enum
import argparse
import logging
log = logging.getLogger(__file__)


class api(Enum):
    complex = 'complex'
    simple = 'simple'
    fares = 'fares'
    plan = 'plan'
    rest = 'rest'

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
            case api.rest:
                return "rest"
        return ret_val


class suites(Enum):
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
