import os
import re
import requests
from ott.utils import file_utils
from ott.utils import web_utils

dir_path = os.path.dirname(os.path.abspath(__file__))


def call_dict(test, num=8, factor=0.25, echo=True, is_json=True):
    """
    """
    ret_val = False

    url = test.get('url')
    size = test.get('size')
    expect = test.get('expect')

    i = p = f = 0
    while i < num:
        r = requests.get(url)
        if r.status_code != 200:
            f += 1
            test['status_code'] = r.status_code
            continue

        #import pdb; pdb.set_trace()
        if expect:
            if expect in r.text:
                p += 1
            else:
                #import pdb; pdb.set_trace()
                if re.search(expect, r.text):
                    p += 1
                else:
                    test['expect_fail'] = True
                    f += 1

        if size:
            if len(r.text) >= int(size):
                p += 1
            else:
                test['size_fail'] = True
                f += 1
        i += 1

    # check that we have plenty of passes and few failures from the service calls above
    acceptable_fails = int(num * factor)
    acceptable_passses = int(num * (1.0 - factor))
    if p >= acceptable_passses and f <= acceptable_fails:
        ret_val = True

    return ret_val


def result(test, is_pass):
    description = test.get('description')
    if is_pass:
        print(f"PASS: {description}")
    else:
        print(f"FAIL: {description}")


def main():
    #web_utils.simple_email("hey", "purcellf@trimet.org")
    p = os.path.join(dir_path, 'uptime.csv')
    tests = file_utils.read_csv(p)
    for t in tests:
        t['url'] = t['url'].replace("ws.", "ws-st.")  # test staging not prod
        res = True
        res = call_dict(t)
        result(t, res)
