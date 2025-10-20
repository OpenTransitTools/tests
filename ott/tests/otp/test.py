from . import test_suite
from .utils import cmdline
from .utils.exe import call_otp

from .utils import cmdline, misc
from .templates import template_utils


def uptime():
    pass


def smoke():
    #import pdb; pdb.set_trace()
    c = cmdline.tora_cmdline("smoke_test")
    l = test_suite.TestSuiteList(c.url, "") # , c.app_url, filter=c.suites)
    print(l)


def all():
    #import pdb; pdb.set_trace()
    c = cmdline.tora_cmdline("all_tests")
    t = template_utils.make_named_template(c.api.find_api())
    l = test_suite.TestSuiteList(c, t, misc.graphql_url, misc.app_url)
    #urls = l.get_webapp_urls(); print('\n\n'.join(urls))
    #l.output_graphql()
    l.output_response()


def plan():
    """ call OTP with a graphql request via cmdline params (note lots of defaults for PDX->ZOO) """
    #import pdb; pdb.set_trace()
    c = cmdline.tora_cmdline()
    t = template_utils.make_named_template(c.api.find_api())
    r = t.render(**vars(c))
    response = call_otp(r, misc.graphql_url)
    if response.status_code == 200:
        o = str(response.json())
    else:
        o = response.text
    print(o)
