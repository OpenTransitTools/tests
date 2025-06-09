from . import test_suite
from .utils import cmdline


def cmd():
    c = cmdline.test_args('smoke tests', do_parse=False)


def main():
    #import pdb; pdb.set_trace()
    c = cmdline.get_args('smoke tests')
    l = test_suite.ListTestSuites(c.url, c.map_url, filter=c.suites)
    if c.stats:
        l.stats()
    if c.print:
        l.printer()
