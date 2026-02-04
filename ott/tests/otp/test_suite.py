from ott.utils.cache_base import CacheBase

from ott.utils import date_utils
from ott.utils import object_utils
from ott.utils import num_utils
from ott.tests.utils import misc
from ott.tests.utils import cmdline
from .exe import call_otp

import os
import sys
import csv
import re
import copy

import time
import logging
log = logging.getLogger(__file__)

MIN_SIZE_ITIN=1000


class TestResult:
    FAIL=000
    WARN=333
    PASS=111


class Test(object):
    """ 
    test object is typically built from a row in an .csv test suite 
    params for test, along with run capability
    """
    def __init__(self, test_suite_file, line_number, csv_params, default_params, graphql_template, graphql_url, app_url):
        self.result = TestResult.FAIL
        self.is_valid = True
        self.diagnosis = ""

        self.graphql_url = graphql_url
        self.app_url = app_url

        self.id = "{}-{}".format(test_suite_file, line_number)
        self.csv_line_number = line_number
        self.description = csv_params.get('Description/notes')
        self.expected = csv_params.get('Expected output')

        self.params = self.make_params(csv_params, default_params)
        self.template = graphql_template
        self.payload = self.make_payload(self.params, graphql_template)
        self.itinerary = ""
        self.json_itinerary = None

    @classmethod
    def make_params(cls, csv_params, default_params):
        """
        csv format: "Description/notes,From,To,Mode,Time,Optimize,Reluctance,Arrive by,Expected output"
          OTP parmas:
            'From'
            'To'
            'Mode'
            'Time'
            'Optimize'
            'Reluctance'
            'Arrive by'

          Test params:
            'Description/notes' describes aspects and reasons for the test
            'Expected output' regex text to find in the OTP response
        """
        ret_val = {}

        # 
        if not default_params:
            #import pdb; pdb.set_trace()
            default_params = cmdline.tora_cmdline()
        ret_val = copy.deepcopy(default_params)

        r = ret_val
        p = csv_params

        # override the 'default' routing params (from cmdline / defaults) with test values from this line of the .csv
        r.fromPlace = object_utils.get_striped_dict_val(p, 'From', r.fromPlace, True, False)
        r.toPlace = object_utils.get_striped_dict_val(p, 'To', r.toPlace, True, False)
        r.time = object_utils.get_striped_dict_val(p, 'Time', r.time, True, False)
        r.time = date_utils.english_to_24hr(r.time)
        r.walkReluctance = object_utils.safe_int(p.get('Reluctance'), r.walkReluctance)
        r.bikeReluctance = object_utils.safe_int(p.get('Reluctance'), r.bikeReluctance)
        r.carReluctance = object_utils.safe_int(p.get('Reluctance'), r.carReluctance)
        r.optimize = p.get('Optimize', r.optimize)
        modes = object_utils.safe_dict_val(p, 'Mode')
        if modes:
            modes = modes.split(',')
            r.transportModes = modes
        ab = object_utils.safe_dict_val(p, 'Arrive by')
        if ab:
            r.arriveBy = True
        return ret_val

    @classmethod
    def make_payload(self, params, template):
        ret_val = template.render(**vars(params))
        return ret_val

    def call_otp_graphql(self):
        """ calls OTP's routing graphql web service """
        self.itinerary = None
        start = time.time()
        response = call_otp(self.payload, self.graphql_url)
        end = time.time()

        if response.status_code == 200:
            self.result = TestResult.PASS
            self.json_itinerary = response.json()
            o = str(self.json_itinerary)
        else:
            self.result = TestResult.FAIL
            o = response.text
        self.itinerary = o

        self.response_time = end - start
        log.info("call_otp: response time of {} seconds for call {}".format(self.response_time, self.description))
        log.debug(self.itinerary)
        if self.response_time > 30:
            self.result = TestResult.WARN
            log.info("call_otp: :::NOTE::: response time took *longer than 30 seconds* for {}".format(self.description))

        return self.itinerary

    def test_expected_response(self, strict=True):
        def regex_search(count_itins=True):
            regres = re.search(self.expected, self.itinerary)
            if regres:
                self.result = TestResult.PASS
                self.diagnosis = "Good: the OTP result had a match for the '{}' regex".format(self.expected)
            else:
                self.result = TestResult.FAIL if strict else TestResult.WARN
                self.diagnosis = "Bad: could NOT find a match for the '{}' regex".format(self.expected)
            if count_itins:
                #import pdb; pdb.set_trace()
                n = len(self.json_itinerary['data']['plan']['itineraries'])
                self.diagnosis = "{} in the {} itinerary(s) returned".format(self.diagnosis, n)

        #import pdb; pdb.set_trace()
        if self.json_itinerary is None:  # should never get here, but just in case have this so we don't NPE below
            log.info("NOTE: this test lacks an expected result {}".format(self.description))
            self.diagnosis = "Bad: OTP response is empty!"
        elif self.result == TestResult.PASS:
            if self.json_itinerary.get('errors'):
                self.result = TestResult.FAIL
                self.diagnosis = "Bad: OTP response has errors:\n  {}".format(self.json_itinerary.get('errors'))
            else:
                j = self.json_itinerary
                if j['data'] and j['data']['plan'] and j['data']['plan']['itineraries'] and len(j['data']['plan']['itineraries']) > 0:
                    if self.expected and len(self.expected) > 1:
                        regex_search()
                    else:
                        self.result = TestResult.PASS
                        self.diagnosis = "Good: OTP responded with {} itinerary(s)!".format(len(j['data']['plan']['itineraries']))
                        log.info("NOTE: this test lacks an expected result {}".format(self.description))
                else:
                    if self.expected and len(self.expected) > 1:
                        regex_search(False)
                    else:
                        self.result = TestResult.FAIL
                        self.diagnosis = "Bad: OTP didn't come back with any itineraries!"
                        log.info("NOTE: this test lacks an expected result {}".format(self.description))

        return self.result == TestResult.FAIL

    def did_test_pass(self):
        return self.result is not None and self.result is TestResult.PASS

    def get_webapp_url(self):
        #https://trimet.org/home/planner-trip/?date=2025-09-15&time=13%3A11&fromPlace=305+NW+Park+Ave%3A%3A45.525261%2C-122.67935&toPlace=839+SE+Yamhill%3A%3A45.515879%2C-122.6574554&arriveBy=false&modes%5B0%5D.mode=BUS&modes%5B1%5D.mode=TRAM&modes%5B2%5D.mode=RAIL&modes%5B3%5D.mode=GONDOLA&searchWindow=14400&walkReluctance=4&walkSpeed=1.34        
        # TODO 'transportModes', 'walkReluctance', {p.bikeReluctance}, 'walkSpeed'}"
        p = self.params

        # step 1: turn list of modes into string ala 'modes[0].mode=RAIL&modes[1].mode=BUS&modes%5B2%5D.mode=TRAM'
        modes = ""
        for i, m in enumerate(p.transportModes):
            sep = "" if i == 0 else "&"
            modes = "{}{}modes[{}].mode={}".format(modes, sep, i, m)

        # step 2: make sure we have a named string
        frm = p.fromPlace if "::" in p.fromPlace else "X::{}".format(p.fromPlace)
        to = p.toPlace if "::" in p.toPlace else "Y::{}".format(p.toPlace)
        
        # step 3: build the url
        url = f"{self.app_url}?date={p.date}&time={p.time}&{modes}&fromPlace={frm}&toPlace={to}&searchWindow={p.searchWindow}&arriveBy={"true" if p.arriveBy else "false"}"
        return url

    def get_result(self, do_html=True):
        ret_val = "PASS" if self.result is TestResult.PASS else "FAIL"
        if do_html:
            ret_val = '<p class="{}">{}</p>'.format(ret_val, ret_val)
        return ret_val

    def get_payload(self, trim=True):
        ret_val = self.payload
        if trim:
            ret_val = misc.trim_lines(self.payload)
        return ret_val

    def get_itinerary(self, trim=None):
        ret_val = self.itinerary
        if trim:
            n = num_utils.to_int(trim, 1000)
            if n > 1 and n < len(self.itinerary):
                ret_val = "{}...".format(self.itinerary[:n])
        return ret_val


class TestSuite(object):
    """ 
    corresponds to a single .csv 'test suite'
    """
    def __init__(self, suite_dir, file, otp_params, graphql_payload, graphql_url, webapp_url):
        self.suite_dir = suite_dir
        self.file = file
        self.file_path = os.path.join(suite_dir, file)
        self.name = file
        self.params = []
        self.tests  = []
        self.failures = 0
        self.passes   = 0
        self.read_csv()
        self.make_tests(otp_params, graphql_payload, graphql_url, webapp_url)

    def read_csv(self, comment="#"):
        """
        read the test suite .csv file (full of test params like from & to)
        and save each row (params) as a set of test params
        """
        with open(self.file_path, 'r') as fp:
            reader = csv.DictReader(filter(lambda row: row[0]!=comment, fp))
            # fn = reader.fieldnames
            for r in reader:
                self.params.append(r)

    def make_tests(self, otp_params, graphql_payload, graphql_url, webapp_url):
        for i, p in enumerate(self.params):
            t = Test(self.file, i+2, p, otp_params, graphql_payload, graphql_url, webapp_url)
            self.tests.append(t)

    def get_tests(self):
        return self.tests

    def run_tests(self, strict=True, progress=True):
        for t in self.get_tests():
            if progress:
                print(".", end='', flush=True)
            g = t.call_otp_graphql()
            r = t.test_expected_response(strict)
            if r:
                self.failures += 1
            else: 
                self.passes += 1
        if progress:
            print()
   
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
        ret_val = []
        for t in self.get_tests():
            ret_val.append(t.get_webapp_url())
        return ret_val


class TestSuiteList(CacheBase):
    """
    """
    def __init__(self, otp_params, graphql_template, graphql_url, webapp_url, suite_dir=None, suites_filter=None):
        """
        """
        self.graphql_template = graphql_template
        self.graphql_url = graphql_url
        self.webapp_url = webapp_url
        self.test_suites = self.make_suites(otp_params, suite_dir, suites_filter)

    @classmethod
    def factory(cls, params=None, template=None):
        if template == None:
            from .templates import template_utils
            template = template_utils.make_named_template('plan_tora')
        return TestSuiteList(params, template, misc.graphql_url, misc.app_url)

    def get_requests(self):
        ret_val = []
        for ts in self.test_suites:
            for t in ts.get_tests():
                ret_val.append(t.payload)
        return ret_val

    def get_latlons(self):
        ret_val = []
        for t in self.test_suites:
            ret_val = ret_val + t.get_latlons()
        return ret_val

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
                t = TestSuite(suite_dir, f, otp_params, self.graphql_template, self.graphql_url, self.webapp_url)
                test_suites.append(t)
        return test_suites

    def get_suites(self):
        return self.test_suites

    def output_graphql(self, stream=sys.stdout, pause=True, trim=True):
        for ts in self.test_suites:
            for t in ts.get_tests():                
                print(t.description, file=stream)
                print(t.get_payload(trim), file=stream)
                if pause:
                    input("\nPress Enter to continue...\n")

    def output_response(self, stream=sys.stdout, pause=True, trim=False):
        for ts in self.test_suites:
            for t in ts.get_tests():
                print(t.description, file=stream)
                print(t.graphql_url, file=stream)
                print(t.get_payload(trim), file=stream)
                t.call_otp_graphql()
                t.get_itinerary(trim)
                print(t.get_itinerary(trim), file=stream)
                if pause:
                    input("\nPress Enter to continue...\n")

    def get_webapp_urls(self):
        ret_val = []
        for ts in self.test_suites:
            u = ts.get_webapp_urls()
            ret_val.extend(u)
        return ret_val

    def get_suites(self):
        return self.test_suites

    def run_tests(self, strict=True, acceptable_num_fails=2):
        for ts in self.test_suites:
            ts.run_tests(strict, acceptable_num_fails)
        return self.has_errors(acceptable_num_fails)

    def has_errors(self, acceptable_num_fails=2):
        #import pdb; pdb.set_trace()
        ret_val = False
        for t in self.test_suites:
            if t.failures > acceptable_num_fails or t.passes <= 0:
                ret_val = True
                break
        return ret_val

    def num_errors(self):
        ret_val = 0
        for t in self.test_suites:
            ret_val += t.failures
        return ret_val

    def num_passes(self):
        ret_val = 0
        for t in self.test_suites:
            ret_val += t.passes
        return ret_val

    def report(self):
        from .templates import template_utils
        t = template_utils.make_named_template("report")
        r = t.render(tsl=self, now=date_utils.pretty_date_time(date_fmt='%m-%d-%Y'), num_passes=self.num_passes(), num_errors=self.num_errors())
        with open('report.html', 'w') as f:
            f.write(r)

    def get_pass_fail_counts(self, html=False):
        ret_val = ""
        for ts in self.test_suites:
            err = "test suite '{}' has {} errors and {} passes".format(ts.name, ts.failures, ts.passes)
            log.info(err)
            if html:
                err = "\n    <li class='msg'>{}</li>".format(err)
            else:
                err += "\n"
            ret_val = ret_val + err
        return ret_val

    def stats(self):
        for ts in self.test_suites:
            ts.stats()
