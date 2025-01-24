"""
run otp via trip plans defined in ./templates/*.mako
"""
import os
import requests
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils
from ott.utils.parse.cmdline import base_cmdline
from .test_suite import ListTestSuites
from . import utils


def call_otp(query, headers=None, url=None):
    if url is None:
        url = utils.url
    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }
    payload = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=payload)
    return response


def make_templates():
    ret_val = []
    tmpl_dir=os.path.join(utils.this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(tmpl_dir, ".mako"):
        #print(t)
        tmpl = Template(filename=t, lookup=tl)
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
    ret_val = []
    requests = make_requests()
    for f in filters:
        for i, t in enumerate(requests):
            if i == f:
                ret_val.append(requests[i])
                break
    return ret_val


def print_request_response(filters, sum):
    requests = filter_requests(filters)
    for i, r in enumerate(requests):
        response = call_otp(r)
        print(f"\n\033[1;4mRequest+Response\033[0m #{filters[i]}:")
        print(str(r)[4:400]) if sum else print(str(r))
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
        type=int, nargs='+',
        default=[1],
        help="filter idz"
    )
    parser.add_argument(
        '--sum',
        '--summarize',
        '-s',
        required=False,
        action="store_true",
        help="summarize results"
    )    
    ret_val = utils.add_cmd_line_util_args(parser)
    return ret_val


def main():
    #import pdb; pdb.set_trace()
    p = make_cmd_line()
    print_request_response(p.filter, p.sum)

