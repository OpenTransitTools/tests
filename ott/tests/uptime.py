import os
from ott.utils import file_utils
from ott.utils import web_utils

dir_path = os.path.dirname(os.path.abspath(__file__))


def main():
    #web_utils.simple_email("hey", "purcellf@trimet.org")
    p = os.path.join(dir_path, 'uptime.csv')
    f = file_utils.read_csv(p)
    print(f)
