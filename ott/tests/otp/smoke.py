from . import test_suite
from .utils import cmdline


def cmd():
    c = cmdline.test_args('smoke tests', do_parse=False)


def main():
    #import pdb; pdb.set_trace()
    c = cmdline.get_args('smoke tests')
    print(c)
    l = test_suite.ListTestSuites(c.url, c.api)
    if c.print:
        l.printer()
