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

 #   def startswith(self, n):
#        return self.value.startswith(n)
        
    def __str__(self):
        return self.value


class suites(Enum):
    all = '*'
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
    parser = argparse.ArgumentParser(
        prog=prog_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--url',    '-u', type=str, default="maps8.trimet.org", help='server to test')
    parser.add_argument('--api',    '-a', type=api, default=api.rest, choices=list(api), help='which OTP api to call')
    parser.add_argument('--suite',  '-s', type=suites, default="*", choices=list(suites), help='csv name of test suite')
    parser.add_argument('--max',    '-m', type=int, default=3000, help='limit to number of tests')
    parser.add_argument('--stats',  '-stats', '-t', action='store_true', help='print test stats')
    parser.add_argument('--print',  '-print', '-p', action='store_true', help='print test urls')
    parser.add_argument('--curl',   '-curl',  '-c', action='store_true', help='"curl" the url (execute the test)')

    if do_parse:
        args = parser.parse_args()
    else:
        args = parser
    return args
