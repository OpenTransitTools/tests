from . import test_suite
from .utils import cmdline
from .templates import template_utils


def smoke():
    #import pdb; pdb.set_trace()
    c = cmdline.get_args('smoke_test')
    l = test_suite.ListTestSuites(c.url, c.app_url, filter=c.suites)


def uptime():
    pass


def all():
    pass

