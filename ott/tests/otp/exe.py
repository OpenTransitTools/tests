"""
run otp via trip plans defined in ./templates/*.mako
"""
import requests
from .test_suite import ListTestSuites
from .utils import cmdline, misc
from .templates import template_utils


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


def plan_trip():
    """ call OTP with a graphql request via cmdline params (note lots of defaults for PDX->ZOO) """
    t = template_utils.make_named_template('plan_tora')
    p = cmdline.tora_cmdline()
    r = t.render(**vars(p))
    #import pdb; pdb.set_trace()
    #print(r); return
    response = call_otp(r)
    if response.status_code == 200:
        o = str(response.json())
    else:
        o = response.text
    print(o)

