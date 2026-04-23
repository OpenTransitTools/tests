import os
import re
import time
import requests
from ott.utils import file_utils
from ott.utils.parse.cmdline import base_cmdline
from . import headless

dir_path = os.path.dirname(os.path.abspath(__file__))


def curl_test(url, expect=None, test={}, size=100):
    ret_val = False

    r = requests.get(url)
    if r.status_code != 200:
        test['status_code'] = r.status_code
    elif expect:
        if expect in r.text:
            ret_val = True
        elif re.search(expect, r.text):
            ret_val = True
        else:
            test['expect_fail'] = True
    elif size:
        if len(r.text) >= int(size):
            ret_val = True
        else:
            test['size_fail'] = True
    else:
         ret_val = True  # no size or expect, so just say true if status code was 200
    return ret_val


def call_dict(test, num=8, factor=0.375, echo=True, is_json=True):
    """
    """
    ret_val = False

    url = test.get('url')
    size = test.get('size')
    expect = test.get('expect')
    is_headless = test.get('headless')

    p = f = 0
    for i in range(num):
        #import pdb; pdb.set_trace()
        passed = headless.browse_and_test(url, expect) if is_headless else curl_test(url, expect, test, size)
        if passed:
            p += 1
            time.sleep(0.5)
        else:
            f += 1
            time.sleep(2.5)
        

    # check that we have plenty of passes (and no more than a few failures) from the service calls above
    acceptable_fails = int(num * factor)
    acceptable_passes = int(num * (1.0 - factor))
    if p >= acceptable_passes and f <= acceptable_fails:
        ret_val = True

    return ret_val


def result(test, is_pass):
    description = test.get('description')
    url = test.get('url', "")
    if is_pass:
        print(f"PASS: {description} - {url}")
    else:
        print(f"FAIL: {description} - {url}")


def do_test(test, staging=False):
    try:
        # test staging not prod
        if staging:
            test['url'] = test['url'].replace("ws.", "ws-st.")

        ret_val = call_dict(test)
    except:
        ret_val = False

    result(test, ret_val)
    return ret_val


def main():
    parser = base_cmdline.empty_parser(f"poetry run uptime")
    parser.add_argument('--staging',  '--st', '-st', action='store_true', help='use staging server ws-st.trimet.org')
    args = parser.parse_args()

    ret_val = 1
    p = os.path.join(dir_path, 'uptime.csv')
    tests = file_utils.read_csv(p)
    for t in tests:
        if do_test(t, args.staging) is False:
            ret_val = 0
    return ret_val
