"""
utils for this project
"""
import os
import inspect

import logging
log = logging.getLogger(__file__)


utils_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
this_module_dir = os.path.dirname(os.path.join(utils_dir, '../'))

url = "http://maps8.trimet.org/rtp/gtfs/v1"
def set_url(u):
    global url
    if u and len(u) > 2:
        if u.upper() == "PROD" or u.upper() == "MAPS":
            url = "https://maps.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "RTP":
            url = "https://ws.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "STAGE":
            url = "https://ws-st.trimet.org/rtp/gtfs/v1"
        elif u.upper() == "TEST":
            url = "http://maps8.trimet.org/rtp/gtfs/v1"
        else:
            url = u


threads = 0
def set_threads(t):
    global threads
    try:
        threads = int(t)
    except:
        pass


def parse_place(pre, place):
    """ 
    break up any PLACE::45.5,-122.5 into name, lat, lon parts
    """
    ret_val = {}
    try:
        name = lat = lon = None
        parts = place.split("::")
        ll = parts[0]
        if len(parts) == 2:
            name = parts[0]
            ll = parts[1]
        ll = ll.split(",")
        lat = ll[0]
        lon = ll[1]
        ret_val = {pre + 'name': name, pre + 'lat': lat, pre + 'lon': lon}
    except Exception as ex:
        log.warning(ex)
    return ret_val


""" methods below dumped here from old exe script """

def filter_requests(filters):
    """ return a dict of filtered requests """
    ret_val = {}
    requests = make_requests()
    for i, r in enumerate(requests):
        for f in filters:
            #import pdb; pdb.set_trace()
            index_filter = num_utils.to_int(f)
            if index_filter is not None:
                if index_filter == i:
                    ret_val[f] = r
            elif len(f) >= 3:
                if f in r:
                    ret_val[f"{f} - #{i}"] = r

    return ret_val


def print_request_response(filters, sum):
    """ """
    requests_dict = filter_requests(filters)
    for id, request in requests_dict.items():
        response = call_otp(request)
        print(f"\n\033[1;4mRequest+Response\033[0m #{id}:")
        print(str(request)[4:400]) if sum else print(str(request))
        if response.status_code == 200:
            n = str(response.json())
            print(n[:1000]) if sum else print(n)
        else:
            print(response.text)
        print("\n\n")
