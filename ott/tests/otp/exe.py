"""
run otp via trip plans defined in ./templates/*.mako
"""
import os
import requests
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils, num_utils, date_utils
from ott.utils.parse.cmdline import base_cmdline
from .test_suite import ListTestSuites
from .utils import misc


def call_otp(query, headers=None, url=None):
    if url is None:
        url = misc.url
    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }
    payload = {
        "query": query
    }
    #print(); print(payload); print()
    response = requests.post(url, headers=headers, json=payload)
    return response


def make_template(file, tl=None):
    ret_val = None
    try:
        #import pdb; pdb.set_trace()    
        if tl is None:
            tmpl_dir=os.path.join(misc.this_module_dir, 'templates')
            tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs inclde
        ret_val = Template(filename=file, lookup=tl)
    except Exception as e:
        pass
    return ret_val


def make_named_template(file_name, tl=None):
    ret_val = None
    tmpl_dir=os.path.join(misc.this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(tmpl_dir, ".mako"):
        if file_name in t:
            tmpl = make_template(t, tl)
            if tmpl:
                ret_val = tmpl
                break
    return ret_val


def make_templates():
    ret_val = []
    tmpl_dir=os.path.join(misc.this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(tmpl_dir, ".mako"):
        tmpl = make_template(t, tl)
        if tmpl:
            #print(t)
            ret_val.append(tmpl)
    return ret_val


def make_requests(templates=None, coords=None):
    """ returns an array of strings, each being a GraphQL request to OTP """
    ret_val = []

    if templates == None:
        templates = make_templates()

    if coords == None:
        l = ListTestSuites("x", "y")
        coords = l.get_latlons()

    for t in templates:
        if coords:
            for c in coords:
                gql = t.render(**c)
                ret_val.append(gql)
        else:
            gql = t.render()
            ret_val.append(gql)

    return ret_val


def filter_requests(filters):
    """ return a dict of filtered requests """
    ret_val = {}
    requests = make_requests()
    for i, r in enumerate(requests):
        for f in filters:
            #import pdb; pdb.set_trace()
            index_filter = num_utils.to_int(f)
            if index_filter is not None:
                if index_filter == i:
                    ret_val[f] = r
            elif len(f) >= 3:
                if f in r:
                    ret_val[f"{f} - #{i}"] = r

    return ret_val


def print_request_response(filters, sum):
    requests_dict = filter_requests(filters)
    for id, request in requests_dict.items():
        response = call_otp(request)
        print(f"\n\033[1;4mRequest+Response\033[0m #{id}:")
        print(str(request)[4:400]) if sum else print(str(request))
        if response.status_code == 200:
            n = str(response.json())
            print(n[:1000]) if sum else print(n)
        else:
            print(response.text)
        print("\n\n")


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
    ret_val = misc.add_cmd_line_util_args(parser)
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

    ret_val = misc.add_url_arg(parser, True)
    return ret_val

def tora():
    p = tora_cmdline()
    t = make_named_template('plan_tora')
    d = vars(p)
    r = t.render(**d)
    #import pdb; pdb.set_trace()
    #print(r); return
    response = call_otp(r)
    if response.status_code == 200:
        o = str(response.json())
    else:
        o = response.text
    print(o)


def main():
    #import pdb; pdb.set_trace()
    p = make_cmd_line()
    print_request_response(p.filter, p.sum)

