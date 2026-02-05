from ott.tests.utils import cmdline
from ott.tests.utils import misc

from . import test_suite
from .exe import call_otp
from .templates import template_utils


def base(name, graphql_url):
    c = cmdline.tora_cmdline(name, graphql_url)
    t = template_utils.make_named_template(c.api.find_api())
    l = test_suite.TestSuiteList(c, t, misc.graphql_url, misc.app_url, suites_filter=c.suites)
    return l


def uptime():
    pass


def smoke():
    #import pdb; pdb.set_trace()
    c = cmdline.tora_cmdline("smoke_test")
    l = test_suite.TestSuiteList(c.url, "")  # , c.app_url, filter=c.suites)
    print(l)


def all(graphql_url=None, report_dir=None):
    #import pdb; pdb.set_trace()
    l = base("otp-all", graphql_url)
    try:
        l.run_tests()
        l.report(dir=report_dir)
    except KeyboardInterrupt:
        print("\n")

    if l.has_errors():
        print(l.get_pass_fail_counts())
    else:
        print("Noice! (no errors)")

    return not l.has_errors()


def misc_test_data():
    l = base("otp-all", None)
    u = l.get_webapp_urls(); print('\n\n'.join(u)) # show URLs to webapp like trimet.org
    l.output_graphql()  # show each test's graphql params
    l.output_response() # call OTP and show response


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
