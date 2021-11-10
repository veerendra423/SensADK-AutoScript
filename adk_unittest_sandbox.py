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
        self.pobj = pexpect.spawn("/bin/bash ./sbox-menu.sh")
        if log == "true":
            self.pobj.logfile = sys.stdout
        a = self.pobj.expect(["Please enter your choice:",pexpect.EOF],timeout=60)
        self.assertTrue(a in [0])
   
    def test_sbox_scli(self):
        self.pobj.sendline("1")
        sbox=self.pobj.expect(["registry ok","registry started",pexpect.EOF],timeout=60)
        self.assertTrue(sbox in [0,1])
        print("registry ok sbox")
  
    def test_verify_mesure(self):
        self.pobj.sendline("2")
        result = self.pobj.expect(['"status": true',pexpect.EOF],timeout=60)
        time.sleep(5)
        self.assertTrue(result == 0)
        if result == 0:
            print("Measurement Successful")
        else:
            print("ERROR at step two")
            sys.exit(-1)

    def test_decryption_keys(self):
        self.pobj.sendline("3")
        decrypt = self.pobj.expect(["Decrypting DataSet decryption Keys ... TBD",pexpect.EOF],timeout=60)
        time.sleep(5)
        self.assertTrue(decrypt == 0)
        print("Decrypting DataSet decryption Keys ... TBD")

    def test_verify_and_decrypt(self):
        self.pobj.sendline("4")
        verify = self.pobj.expect(['"status": true',pexpect.EOF],timeout=60)
        time.sleep(5)
        self.assertTrue(verify == 0)
        if verify == 0:
            print("Signature Verified, Decrypted")
        else:
            print("ERROR at step four")
            sys.exit(-1)

    def test_run_image(self):
        self.pobj.sendline("5")
        run = self.pobj.expect(["loss",pexpect.EOF],timeout=60)
        time.sleep(3)
        self.assertTrue(run == 0)
        print("image ran successfully")


if __name__ == '__main__':
  #  unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner())
 #   runner = unittest.TextTestRunner(verbosity=2,failfast=True)
#    runner.run(suite())
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestSbox('test_sbox_scli'))
    test_suit.addTest(TestSbox('test_verify_mesure'))
    test_suit.addTest(TestSbox('test_decryption_keys'))
    test_suit.addTest(TestSbox('test_verify_and_decrypt'))
    test_suit.addTest(TestSbox('test_run_image'))

    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report_sbox").run(test_suit)

