"""
call a website using a headless browser
"""
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

import logging


def browse_and_test(url, expect_strs=[]):
    ret_val = True

    # sanitize any test strings into workable list for the loop below
    #import pdb; pdb.set_trace()
    if not expect_strs:
        expect_strs = []
    elif not isinstance(expect_strs, list):
        expect_strs = [expect_strs]

    def do_test(page, test_str, count=1, timeout=3000):
        nonlocal ret_val
        try:
            expect(page.get_by_text(test_str)).to_have_count(count=count, timeout=timeout)
        except Exception as e:
            logging.warning(e)
            ret_val = False

    with sync_playwright() as p:
        # chromium headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        logging.info(page.title())
        for e in expect_strs:
            do_test(page, e)
        browser.close()

    return ret_val


def example():
    url = "https://trimet.org/home/planner-trip/?fromPlace=435+NW+6th+Ave%3A%3A45.52672003%2C-122.6768376&toPlace=1900+SW+4th+Ave%3A%3A45.510422%2C-122.6804610"
    if browse_and_test(url, ["Option 1", "Option 3"]):
        print("pass")
    else:
        print("fail")

    url = "https://trimet.org/home/route/TRIMET:2"
    browse_and_test(url, ["To Gresham", "To Portland"])

    url = "https://trimet.org/home/stop/TRIMET:2"
    browse_and_test(url, ["A Ave & Chandler", "78-Denney"])
