from . import test_suite
from .utils import cmdline
from .templates import template_utils


def cmd():
    c = cmdline.test_args('smoke tests', do_parse=False)


def curl_test(api, lts):
    import pdb; pdb.set_trace()
    t = template_utils.make_named_template(api.find_api())
    print(t)
    lts.stats()


def main():
    #import pdb; pdb.set_trace()
    c = cmdline.get_args('smoke tests')
    l = test_suite.ListTestSuites(c.url, c.map_url, filter=c.suites)
    if c.stats:
        l.stats()
    if c.print:
        l.printer()
    if c.curl:
        curl_test(c.api, l)
