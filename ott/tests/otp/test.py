from . import test_suite
from .utils import cmdline
from .utils.exe import call_otp

from .utils import cmdline, misc
from .templates import template_utils


def smoke():
    #import pdb; pdb.set_trace()
    c = cmdline.tora_cmdline("smoke_test")
    l = test_suite.ListTestSuites(c.url, "") # , c.app_url, filter=c.suites)
    print(l)


def uptime():
    pass


def all():
    pass


def plan():
    """ call OTP with a graphql request via cmdline params (note lots of defaults for PDX->ZOO) """
    t = template_utils.make_named_template('plan_tora')
    p = cmdline.tora_cmdline()
    r = t.render(**vars(p))
    #import pdb; pdb.set_trace()
    #print(r); return
    response = call_otp(r, misc.url)
    if response.status_code == 200:
        o = str(response.json())
    else:
        o = response.text
    print(o)
