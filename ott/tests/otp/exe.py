"""
run otp via trip plans defined in ./templates/*.mako
"""
import os
import requests
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils, num_utils
from .test_suite import ListTestSuites
from .utils import cmdline, misc


def call_otp(query, headers=None, url=None):
    """ """
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


def tora():
    """ """
    p = cmdline.tora_cmdline()
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
    #print_request_response(p.filter, p.sum)

