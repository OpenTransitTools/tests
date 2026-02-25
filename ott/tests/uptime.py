import os
from ott.utils import file_utils
from ott.utils import web_utils

dir_path = os.path.dirname(os.path.abspath(__file__))


def call(url, size=None, expect=None, num=6, factor=2, echo=True):
    """
    """
    ret_val = False

    i = p = f = 0
    while i < num:
        
        if expect:
            p += 1
            f += 1

        if size:
            p += 1
            f += 1

        i += 1



    return ret_val


def main():
    #web_utils.simple_email("hey", "purcellf@trimet.org")
    p = os.path.join(dir_path, 'uptime.csv')
    f = file_utils.read_csv(p)
    print(f)
