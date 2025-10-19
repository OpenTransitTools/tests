from ott.utils.cache_base import CacheBase

from ott.utils import otp_utils
from ott.utils import date_utils
from ott.utils import object_utils
from .utils import misc

import os
import sys
import csv
import re

import time
import datetime
import logging
log = logging.getLogger(__file__)

MIN_SIZE_ITIN=1000


class TestResult:
    FAIL=000
    WARN=333
    PASS=111


class OListTestSuites(CacheBase):
    """
    TODO
    """
    def __init__(self, otp_params, graphql_url, webapp_url, suite_dir=None, suites_filter=None):
        """ """
        #import pdb; pdb.set_trace()
        self.graphql_url = graphql_url
        self.webapp_url = webapp_url
        self.test_suites = self.make_suites(otp_params, suite_dir, suites_filter)

    def make_suites(self, otp_params, suite_dir, filter):
        """ load test_suites .csv files """
        test_suites = []

        if suite_dir is None:
            suite_dir = self.sub_dir('test_suites/trimet')

        files = os.listdir(suite_dir)
        for f in files:
            if f.lower().endswith('.csv'):
                if filter and re.match('.*({})'.format(filter), f, re.IGNORECASE) is None:
                    continue
                t = TestSuite(otp_params, suite_dir, f) # TODO , copy.deepcopy(otp_params))
                test_suites.append(t)
        return test_suites

    def has_errors(self, acceptable_num_fails=2):
        ret_val = False
        for t in self.test_suites:
            if t.failures > acceptable_num_fails or t.passes <= 0:
                ret_val = True
                break
        return ret_val

    def list_errors(self):
        ret_val = ""
        if self.has_errors():
            for t in self.test_suites:
                if t.failures > 0 or t.passes <= 0:
                    err = "test suite '{0}' has {1} error(s) and {2} passes\n".format(t.name, t.failures, t.passes)
                    ret_val = ret_val + err
                    log.info(err)
        return ret_val

    def get_suites(self):
        return self.test_suites

    def run(self, run_test=True):
        for ts in self.test_suites:
            ts.run(self.graphql_url, self.webapp_url, self.date, run_test)

    def stats(self):
        for ts in self.test_suites:
            ts.stats()

    def to_url_list(self):
        ret_val = []
        for ts in self.test_suites:
            urls = ts.run(self.graphql_url, self.webapp_url, self.date, run_test=False)
            ret_val.extend(urls)
        return ret_val

    def get_latlons(self):
        """ return a bulk list of broken out coordinate parts """
        ret_val = []
        for ts in self.test_suites:
            ll = ts.get_latlons()
            ret_val.extend(ll)
        return ret_val


class OTest(object):
    """ 
    test object is typically built from a row in an .csv test suite 
    params for test, along with run capability
    """
    def __init__(self, param_dict, line_number, graphql_url, app_url, date=None):
        """ {
            OTP parmas:
              'From'
              'To'
              'Reluctance'
              'Mode'
              'Optimize'
              'Time'

            Test params:
              'Arrive by' - expects 'FALSE' if arrive by test should not be ran or leave empty
              'Expected output'

            Misc text:
              'Description/notes'
            }
        """
        self.config = ConfigUtil(section='otp')

        self.is_valid        = True
        self.error_descript  = None

        self.result          = TestResult.FAIL
        self.response_time   = -1.0

        self.graphql_url     = graphql_url
        self.app_url         = app_url

        self.csv_line_number = line_number
        self.csv_params      = param_dict
        self.date            = date

        self.itinerary       = None
        self.otp_params      = ''
        self.app_params      = ''

        self.description     = self.get_param('Description/notes')
        self.coord_from      = self.get_param('From')
        self.coord_to        = self.get_param('To')
        self.mode            = self.get_param('Mode')
        self.time            = self.get_param('Time', strip_all_spaces=True)
        self.optimize        = self.get_param('Optimize')
        self.reluctance      = self.get_param('Reluctance')
        self.arrive_by       = self.get_param('Arrive by')
        self.expect_output   = self.get_param('Expected output')
 
        # post process the load ... make params and urls, etc...
        self.date = self.get_date_param(self.date)
        self.init_url_params()
        self.url_mode()
        self.url_optimize()
        self.url_time()
        self.url_param('ignoreRealtimeUpdates', 'true')

    def did_test_pass(self):
        return self.result is not None and self.result is TestResult.PASS

    def get_param(self, name, def_val=None, strip_all_spaces=False, warn_not_avail=True):
        return object_utils.get_striped_dict_val(self.csv_params, name, def_val, strip_all_spaces, warn_not_avail)

    def append_note(self, note=None):
        if note:
            self.description = "{}{}".format(self.description, note)

    def test_otp_result(self, strict=True):
        """ regexp test of the itinerary output for certain strings """
        #import pdb; pdb.set_trace()
        if self.itinerary is None:
            self.result = TestResult.FAIL if strict else TestResult.WARN
            self.error_descript = "test_otp: itinerary is null"
        else:
            if len(self.itinerary) < MIN_SIZE_ITIN:
                self.result = TestResult.FAIL if strict else TestResult.WARN
                self.error_descript = "test_otp: looks small at {} characters".format(len(self.itinerary))
            else:
                # result properly sized ... now look for matches to expected data, etc...
                self.error_descript = "test_otp: size {} characters.".format(len(self.itinerary))
                self.test_expected_response(self.expect_output, strict)

        if self.result == TestResult.FAIL:
            log.warning(self.error_descript + "\n  " + self.get_graphql_url())

        return self.result

    def test_expected_response(self, expected_output, strict):
        ret_val = False
        if expected_output is not None and len(expected_output) > 0:
            regres = re.search(expected_output, self.itinerary)
            if regres is None:
                self.result = TestResult.FAIL if strict else TestResult.WARN
                self.error_descript += " - couldn't find " + expected_output + " in otp response"
                ret_val = True
        return ret_val

    def init_url_params(self):
        self.otp_params = 'fromPlace={0}&toPlace={1}'.format(self.coord_from, self.coord_to)

        self.app_params = self.otp_params
        if self.coord_from is None or self.coord_from == '' or self.coord_to is None or self.coord_to == '':
            self.error_descript = "no from and/or to coordinate for the otp url (skipping test) - from:{} to:{}".format(self.coord_from, self.coord_to)
            if self.expect_output:
                log.warning(self.error_descript)
            self.is_valid = False

    def url_param(self, name, param, default=None):
        p = param if param else default
        if p:
            self.otp_params += '&{0}={1}'.format(name, p)
            self.app_params += '&{0}={1}'.format(name, p)

    def url_mode(self, mode=None):
        self.url_param('mode', mode, self.mode)

    def url_optimize(self, opt=None):
        self.url_param('optimize', opt, self.optimize)

    def url_arrive_by(self, opt="true"):
        self.url_param('arriveBy', opt, self.optimize)

    def url_time(self, time=None):
        self.url_param('time', time, self.time)

    def url_time_7am(self):
        self.url_param('time', '7:00am')

    def url_time_12pm(self):
        self.url_param('time', '12:00pm')

    def url_time_5pm(self):
        self.url_param('time', '5:00pm')

    def get_date_param(self, date, fmt="%Y-%m-%d"):
        """ provide a default date (set to today) if no service provided... """
        if self.otp_params.find('date') < 0:
            if date is None:
                date = datetime.datetime.now().strftime(fmt)
            
            self.url_param('date', date)
        return date

    def arrive_by_check(self):
        if self.arrive_by == 'FALSE':
            self.is_valid = False

    def call_otp(self, url=None):
        """ calls the trip web service """
        self.itinerary = None
        start = time.time()
        url = url if url else self.get_graphql_url()
        url = self.fix_url(url)
        self.itinerary = otp_utils.call_planner_svc(url)
        end = time.time()
        self.response_time = end - start
        log.info("call_otp: response time of {} second for url {}".format(self.response_time, url))
        log.debug(self.itinerary)
        if self.response_time <= 30:
            self.result = TestResult.PASS
        else:
            self.result = TestResult.WARN
            log.info("call_otp: :::NOTE::: response time took *longer than 30 seconds* for url {}".format(url))

    def fix_url(self, url):
        """
        this routine will clean up parameter values in a url
        e.g., OTP 2.x throws an exception on optimize=BLAH, when BLAH is unknown to OTP (like TRANSFERS), 
              so this routine cleans that
        """
        ret_val = url
        try:
            if self.is_call() and "optimize=TRANSFERS" in url:
                ret_val = url.replace("optimize=TRANSFERS", "optimize=QUICK")
        except Exception as e:
            log.warning(e)
        return ret_val

    def is_call(self):
        return "otp_ct" in self.graphql_url or "otp_call_REMOVE-ME-WHEN-DEPLOYED" in self.graphql_url

    @classmethod
    def make_url(cls, url, separater="?submit&module=planner"):
        ret_val = url
        if ret_val is None:
            ret_val = "ERROR ERROR ERROR in test_suite.py line 284 ERROR ERROR ERROR"
        else:
            if not ret_val.startswith('http'):
                ret_val = "http://{}".format(url)
            if "?" not in ret_val:
                ret_val = "{}{}".format(ret_val, separater)
        return ret_val

    def get_graphql_url(self):
        # import pdb; pdb.set_trace()
        # OTP needs *BOTH* a date and time parameter ... if you only have time, the request will fail
        if "time=" in self.otp_params and "date=" not in self.otp_params:
            d = date_utils.today_str()
            self.url_param('date', d)
        ret_val = "{}&{}".format(self.make_url(self.graphql_url), self.otp_params)
        ret_val = self.fix_url(ret_val)
        return ret_val

    def get_webapp_url(self):
        return "{}&{}&debug_layers=true".format(self.make_url(self.app_url), self.app_params)

    def get_otpRR_url(self):
        """
        calltaker/otp-react-redux UI has a different url path, along with some unique parameter values
        eg:
          http://call-test.trimet.org/#/?fromPlace=PDX...
            time=13:45
            mode=BUS,TRAM,RAIL,GONDOLA,WALK
        """
        #import pdb; pdb.set_trace()
        arrive = 'true' if self.arrive_by or 'arriveBy=true' in self.otp_params else 'false'
        time = date_utils.english_to_24hr(self.time)
        mode =  otp_utils.breakout_transit_modes(self.mode)
        params = "sessionId=test&fromPlace={}&toPlace={}&time={}&arriveBy={}&mode={}&ui_activeItinerary=0&ui_activeSearch=TEST".format(
            self.coord_from, self.coord_to, time, arrive, mode
        )
        ret_val = "{}{}".format(self.make_url(self.app_url, "#/?"), params)
        return ret_val

    def make_webapp_url(self):
        return "http://maps.trimet.org?submit&" + self.app_params


class OTestSuite(object):
    """ 
    corresponds to a single .csv 'test suite'
    """
    def __init__(self, default_params, suite_dir, file):
        self.suite_dir = suite_dir
        self.file = file
        self.file_path = os.path.join(suite_dir, file)
        self.name = file
        self.default_params = default_params,
        self.params = []
        self.tests  = []
        self.failures = 0
        self.passes   = 0
        self.read()

    def read(self):
        """
        read a .csv file, and save each row as a set of test params
        """
        file = open(self.file_path, 'r')
        reader = csv.DictReader(file)
        fn = reader.fieldnames
        for row in reader:
            self.params.append(row)

    def get_tests(self):
        return self.tests

    def do_test(self, t, strict=True, num_tries=5, run_test=True, print_url=True):
        if t.is_valid:
            if run_test:
                for i in range(1, num_tries):
                    t.call_otp()
                    time.sleep(1)
                    if t.itinerary and len(t.itinerary) > MIN_SIZE_ITIN:
                        break
                    time.sleep(i)
            else:
                t.result = TestResult.PASS

            if run_test:
                t.test_otp_result(strict)
                self.tests.append(t)
                if t.result is TestResult.PASS:
                    self.passes += 1
                elif t.result is TestResult.FAIL:
                    log.info("test_suite: this test failed " + t.get_graphql_url() + "\n")
                    self.failures += 1
                sys.stdout.write(".")
            elif print_url:
                print(t.get_otpRR_url())
            
    def run(self, graphql_url, webapp_url, date=None, run_test=True, print_url=True):
        """ 
        iterate the list of tests from the .csv files, run the test (call otp), and check the output.
        """

        # return values for both arrive and depart urls
        ret_val=[]

        log.info("test_suite {0}: ******* date - {1} *******\n".format(self.name, datetime.datetime.now()))
        for i, p in enumerate(self.params):
            t = Test(p, i+2, graphql_url, webapp_url, date)
            if t.is_valid is False:
                continue

            ret_val.append(t.get_graphql_url())
            self.do_test(t, run_test=run_test, print_url=print_url)

            """ arrive by tests """
            t = Test(p, i+2, graphql_url, webapp_url, date)
            t.url_arrive_by()
            t.append_note(" ***NOTE***: arrive by test ")
            t.arrive_by_check()
            ret_val.append(t.get_graphql_url())
            self.do_test(t, False, run_test=run_test, print_url=print_url)

        return ret_val

    def printer(self, graphql_url, webapp_url, date):
        ret_val = ""
        urls = self.run(graphql_url, webapp_url, date, run_test=False)
        for u in urls:
            ret_val = ret_val + u + "\n"
        return ret_val
    
    def stats(self):
        if not self.tests:
            urls = self.run("", "", "", run_test=False, print_url=False)
            print("{} = {} tests".format(self.name, len(urls)))
        else:
            print("{} = {} tests (passes {})".format(self.name, len(self.tests), self.passes))

    def get_latlons(self):
        """
        returns a dict with from and to coord broken out, ala:
        {'fname': '9790', 'flat': '45.549', 'flon': '-122.91', 'tname': '8550', 'tlat': '45.528', 'tlon': '-122.969'}
        """
        ret_val = []
        for p in self.params:
            f = object_utils.get_striped_dict_val(p, 'From')
            t = object_utils.get_striped_dict_val(p, 'To')
            ff = misc.parse_place('f', f)
            tt = misc.parse_place('t', t)
            ret_val.append({**ff, **tt})
        return ret_val

    def get_webapp_urls(self):
        """
        """
        ret_val = []


class Test(object):
    """ 
    test object is typically built from a row in an .csv test suite 
    params for test, along with run capability
    """
    def __init__(self, line_number, csv_params, default_params, graphql_url, app_url):
        """ {
            OTP parmas:
              'From'
              'To'
              'Reluctance'
              'Mode'
              'Optimize'
              'Time'

            Test params:
              'Arrive by' - expects 'FALSE' if arrive by test should not be ran or leave empty
              'Expected output'

            Misc text:
              'Description/notes'
            }
        """
        self.result = TestResult.FAIL
        self.error_descript  = ""
        self.is_valid = True

        self.graphql_url = graphql_url
        self.app_url = app_url

        self.id = line_number
        self.description = csv_params.get('Description/notes')
        self.expected = csv_params.get('Expected output')

        self.params = self.make_params(csv_params, default_params)

    @classmethod
    def make_params(cls, csv_params, default_params):
        "Description/notes,From,To,Mode,Time,Optimize,Reluctance,Arrive by,Expected output"
        #import pdb; pdb.set_trace()
        import copy
        ret_val = copy.deepcopy(default_params)
        r = ret_val
        p = csv_params

        r.fromPlace = object_utils.get_striped_dict_val(p, 'From', r.fromPlace, True, False)
        r.toPlace = object_utils.get_striped_dict_val(p, 'To', r.toPlace, True, False)
        r.time = object_utils.get_striped_dict_val(p, 'Time', r.time, True, False)
        r.time = date_utils.english_to_24hr(r.time)
        r.arriveBy = object_utils.safe_dict_val(p, 'Arrive by', r.arriveBy)
        return ret_val

    def get_graphql_payload(self, template):
        ret_val = template.render(**vars(self.params))
        return ret_val

    def get_webapp_url(self):
        #https://trimet.org/home/planner-trip/?date=2025-09-15&time=13%3A11&fromPlace=305+NW+Park+Ave%3A%3A45.525261%2C-122.67935&toPlace=839+SE+Yamhill%3A%3A45.515879%2C-122.6574554&arriveBy=false&modes%5B0%5D.mode=BUS&modes%5B1%5D.mode=TRAM&modes%5B2%5D.mode=RAIL&modes%5B3%5D.mode=GONDOLA&searchWindow=14400&walkReluctance=4&walkSpeed=1.34

        # modes[0].mode=RAIL&modes[1].mode=BUS&modes%5B2%5D.mode=TRAM
        # TODO 'transportModes', 'walkReluctance', {p.bikeReluctance}, 'walkSpeed'}"
        p = self.params
        ret_val = f"{self.app_url}?fromPlace={p.fromPlace}&toPlace={p.toPlace}&date={p.date}&time={p.time}&searchWindow={p.searchWindow}&arriveBy={"true" if p.arriveBy else "false"}"
        return ret_val


class TestSuite(object):
    """ 
    corresponds to a single .csv 'test suite'
    """
    def __init__(self, suite_dir, file, otp_params, graphql_url, webapp_url):
        self.suite_dir = suite_dir
        self.file = file
        self.file_path = os.path.join(suite_dir, file)
        self.name = file
        self.params = []
        self.tests  = []
        self.failures = 0
        self.passes   = 0
        self.read_csv()
        self.make_tests(otp_params, graphql_url, webapp_url)

    def read_csv(self):
        """
        read the test suite .csv file (full of test params like from & to)
        and save each row (params) as a set of test params
        """
        file = open(self.file_path, 'r')
        reader = csv.DictReader(file)
        fn = reader.fieldnames
        for row in reader:
            self.params.append(row)

    def make_tests(self, otp_params, graphql_url, webapp_url):
        for i, p in enumerate(self.params):
            t = Test(i+2, p, otp_params, graphql_url, webapp_url)
            self.tests.append(t)

    def get_tests(self):
        return self.tests

    def run_test(self, t, strict=True, num_tries=5, run_test=True, print_url=True):
        pass
    
    def stats(self):
        pass

    def get_latlons(self):
        """
        returns a dict with from and to coord broken out, ala:
        {'fname': '9790', 'flat': '45.549', 'flon': '-122.91', 'tname': '8550', 'tlat': '45.528', 'tlon': '-122.969'}
        """
        ret_val = []
        for p in self.params:
            f = object_utils.get_striped_dict_val(p, 'From')
            t = object_utils.get_striped_dict_val(p, 'To')
            ff = misc.parse_place('f', f)
            tt = misc.parse_place('t', t)
            ret_val.append({**ff, **tt})
        return ret_val

    def get_webapp_urls(self):
        ret_val = []
        for t in self.get_tests():
            ret_val.append(t.get_webapp_url())
        return ret_val



class TestSuiteList(CacheBase):
    """
    TODO
    """
    def __init__(self, graphql_template, otp_params, graphql_url, webapp_url, suite_dir=None, suites_filter=None):
        """ """
        self.graphql_template = graphql_template
        self.graphql_url = graphql_url
        self.webapp_url = webapp_url
        self.test_suites = self.make_suites(otp_params, suite_dir, suites_filter)

    def make_suites(self, otp_params, suite_dir, filter):
        """ load test_suites .csv files """
        test_suites = []

        if suite_dir is None:
            suite_dir = self.sub_dir('test_suites/trimet')

        files = os.listdir(suite_dir)
        for f in files:
            if f.lower().endswith('.csv'):
                if filter and re.match('.*({})'.format(filter), f, re.IGNORECASE) is None:
                    continue
                t = TestSuite(suite_dir, f, otp_params, self.graphql_url, self.webapp_url)
                test_suites.append(t)
        return test_suites

    def get_suites(self):
        return self.test_suites

    def output_graphql(self, stream=sys.stdout, pause=True, trim=True):
        for ts in self.test_suites:
            for t in ts.get_tests():                
                print(t.description, file=stream)
                p = t.get_graphql_payload(self.graphql_template)
                if trim:
                    p = misc.trim_lines(p)
                print(p, file=stream)
                if pause:
                    input("\nPress Enter to continue...\n")

    def get_webapp_urls(self):
        ret_val = []
        for ts in self.test_suites:
            u = ts.get_webapp_urls()
            ret_val.extend(u)
        return ret_val
