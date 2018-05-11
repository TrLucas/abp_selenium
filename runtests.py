#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

original = os.environ['PATH']
os.environ['PATH'] = original + ':' + os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'driver')
)

def run_tests(ext_path):
    chrome_options = Options()
    chrome_options.add_argument("load-extension=" + ext_path);

    # Running extensions in headless chrome is not possible right now.
    # https://bugs.chromium.org/p/chromium/issues/detail?id=706008
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('chrome://extensions/')

    # Close "ABP added" tab.
    driver.switch_to.window(driver.window_handles[1])
    driver.close()

    # Find options-link for ABP.
    driver.switch_to.window(driver.window_handles[0])
    elem = driver.find_element_by_class_name('options-link')

    # Go to options page and run unittests.
    elem.click()
    driver.switch_to.window(driver.window_handles[1])
    driver.execute_script('location.href = "qunit/index.html";')

    # Wait until tests started running (i.e. 'qunit-testresult' is available).
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'qunit-testresult'))
    )

    # Wait for the tests to finish.
    result_elem = driver.find_element_by_id('qunit-testresult')
    result = result_elem.get_attribute('innerHTML')
    while 'Tests completed' not in result:
        time.sleep(1)
        result = result_elem.get_attribute('innerHTML')

    exit_code = 0

    # Find all failed tests.
    failed = driver.find_elements_by_css_selector(
        '#qunit-tests .fail .test-name'
    )
    if failed:
        failed_tests = '\n'.join(x.get_attribute('innerHTML') for x in failed)
        print('FAILED TESTS:\n' + failed_tests)
        exit_code = 1
    else:
        print('All tests passed!')
    driver.quit()
    return exit_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to devenv for Chrome')

    args = parser.parse_args()
    run_tests(args.path)
