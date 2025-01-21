"""
run otp via trip plans defined in ./templates/*.mako
"""
import os
import inspect
import requests
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils
from test_suite import ListTestSuites

def_url = "http://maps8.trimet.org/rtp/gtfs/v1"
#def_url = "https://maps.trimet.org/rtp/gtfs/v1"
this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def call_otp(query, url=def_url):
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
    tmpl_dir=os.path.join(this_module_dir, 'templates')
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


def xmain():
    tmpl_dir=os.path.join(this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])
    #tmpl = Template(filename=os.path.join(tmpl_dir, 'plan_connection_complex.mako'), lookup=tl)
    #tmpl = Template(filename=os.path.join(this_module_dir, 'templates', 'plan_connection_fares.mako'))
    tmpl = Template(filename=os.path.join(tmpl_dir, 'plan_simple.mako'), lookup=tl)
    #request = tmpl.render(flat="45.5552", flon="-122.6534", tlat="45.4908", tlon="-122.5519", skip_geom=True)
    request = tmpl.render()
    #print(request)
    response = call_otp(request)
    print(response.text)
    #tmpl_dir=os.path.join(this_module_dir, 'templates')
    #print(file_utils.find_files(tmpl_dir, ".mako"))

def ymain():
    templates = make_templates()
    request = templates[3].render()
    response = call_otp(request)

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def zmain():
    for r in make_requests():
        response = call_otp(r)
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)

def kmain():
    for r in make_requests():
        print(r)


main=xmain