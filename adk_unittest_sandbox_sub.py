import subprocess
import HtmlTestRunner
import unittest
import pexpect
import sys
import time
import os
import os.path
import ConfigParser
cfg = ConfigParser.ConfigParser()
cfg.read('../client/adk.ini')
log = cfg.get('adk', 'log')
print(log)

class TestSbox(unittest.TestCase):

    def setUp(self):
        print('pass') 
    def test_run_image(self):
        psub = subprocess.call(['bash', '-c', 'source sbox-menu.sh && run_all'])

if __name__ == '__main__':
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestSbox('test_run_image'))
    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report_sbox").run(test_suit)

