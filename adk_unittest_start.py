import HtmlTestRunner
import unittest
import pexpect
import sys
import time
import os
import os.path
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('adk.ini')

x = cfg.get('adk', 'step_one')
y = cfg.get('adk', 'step_two')
z = cfg.get('adk', 'step_three')
w = cfg.get('adk', 'step_four')
log = cfg.get('adk', 'log')

print(x)
print(y)
print(z)
print(w)
print(log)
class TestScliPositive(unittest.TestCase):

    def setUp(self):
        self.pobj = pexpect.spawn("/bin/bash ./scli-menu.sh")
        if log == "true":
            self.pobj.logfile = sys.stdout

        a = self.pobj.expect(["Please review SCLI_ROOT setting in config file and restart","(false)","(true)","Please export GCS_CREDS_FILE_NAME and try again","does not exist - try again when you have it","Please enter your choice:",pexpect.EOF])
        self.assertTrue(a in [0,1,2,3,4,5])
        if a == 0:
            print("Please review SCLI_ROOT setting in config file and restart")
            sys.exit(-1)
        elif a == 1:
            print("ADK in api mode")
        elif a == 2:
            print("ADK in standalone mode")
        elif a == 3:
            print("Please export GCS_CREDS_FILE_NAME and try again")
            sys.exit(-1)
        elif a == 4:
            print("does not exist - try again when you have it")
            sys.exit(-1)
        elif a == 5:
            print("Please enter your choice:")
        else:
            print("ERROR")

    def test_setup_scli(self):
        """
        Test for scli setup
        """
        self.pobj.sendline("1")
        set_up = self.pobj.expect(["Do you want to re-encrypt the dataset?","Success: Create Input DataSet","Skipping encrypt input data in standalone mode","Are you logged into the Sensoriant registry?",pexpect.EOF],timeout=420)
        self.assertTrue(set_up in [0,1,2,3])
        if set_up == 0:
            #self.pobj.sendline('y')
            self.pobj.sendline(x)
            pushed = self.pobj.expect(["aborting re-encrypt ...","Success: Create Input DataSet",pexpect.EOF],timeout=120)
            self.assertTrue(pushed in [0,1])
            print("Success: Create Input DataSet")
        elif set_up == 1:
            time.sleep(10)
            print("Success: Create Input DataSet")
        elif set_up == 2:
            print("Skipping encrypt input data in standalone mode")
        elif set_up == 3:
            print("Are you logged into the Sensoriant registry?")
            self.pobj.sendline('y')
            sens = self.pobj.expect(["Success: Create Input DataSet",pexpect.EOF],timeout==300)
            self.assertEqual(sens, 0)
            print("Success: Create Input DataSet")
            if sens == 0:
                time.sleep(10)

    def test_re_encrypt(self):
        self.pobj.sendline("2")
        result = self.pobj.expect(["Do you want to re-encrypt the dataset?","Success: Create Input DataSet",pexpect.EOF],timeout=60)
        self.assertTrue(result in [0,1])
        #self.pobj.sendline('y')
        if result == 0:
            self.pobj.sendline(y)
            r=self.pobj.expect(["aborting re-encrypt ...","Success: Create Input DataSet",pexpect.EOF],timeout=300)
            self.assertTrue(r in [0,1])
            if r == 0:
                print("aborting re-encrypt ...")
            elif r == 1:
                print("Success: Create Input DataSet")
            else:
                print("ERROR at step two")
                sys.exit(-1)
        elif result == 1:
            print("Skipping encrypt input data in standalone mode")
        else:
            print("ERROR")
            sys.exit(-1)

    def test_switch_build(self):
        self.pobj.sendline("3")
        self.pobj.expect("(number or quit)")
        #self.pobj.sendline("q")
        self.pobj.sendline(z)
        build = self.pobj.expect(["aborting switch ...","Success: Switch Build",pexpect.EOF])
        self.assertTrue(build in [0,1])
        if build == 0:
           print("aborting switch ...")
        elif build == 1:
           print("Success: Switch Build")
        else:
           print("ERROR while build number changing")
           sys.exit(-1)

    def test_newbuild_genalgokey(self):
        self.pobj.sendline("4")
        new_build = self.pobj.expect(["Build number not available!!","number and switch to it?","Success: Generate Output Decryption Key",pexpect.EOF],timeout=700)
        self.assertTrue(new_build in [1,2])
        if new_build == 0:
            print("Build number not available")
        elif new_build == 1:
            #self.pobj.sendline('y')
            self.pobj.sendline(w)
            new_build_check = self.pobj.expect(["aborting new build ...","Success: Generate Output Decryption Key",pexpect.EOF],timeout=700)
            self.assertTrue(new_build_check in [0,1])
            if new_build_check == 0:
                print("aborting new build ...")
            elif new_build_check == 1:
                print("Success: Generate Output Decryption Key")
                time.sleep(10)
            else:
                print("ERROR at building new image")
                sys.exit(-1)
        elif new_build == 2:
            print("Success: Generate Output Decryption Key")
            time.sleep(5)
        else:
            print("error at Build_New_Image_and_Gen_Algo_Keys")
            sys.exit(-1)

class TestScliNegative(unittest.TestCase):

    def setUp(self):
        self.pobj = pexpect.spawn("/bin/bash ./scli-menu.sh")
        #self.pobj.logfile = sys.stdout
        a = self.pobj.expect(["Please review SCLI_ROOT setting in config file and restart","(false)","(true)","Please export GCS_CREDS_FILE_NAME and try again","does not exist - try again when you have it","Please enter your choice:",pexpect.EOF])
        self.assertTrue(a in [0,1,2,3,4,5])
        if a == 0:
            print("Please review SCLI_ROOT setting in config file and restart")
            sys.exit(-1)
        elif a == 1:
            print("ADK in api mode")
        elif a == 2:
            print("ADK in standalone mode")
        elif a == 3:
            print("Please export GCS_CREDS_FILE_NAME and try again")
            sys.exit(-1)
        elif a == 4:
            print("does not exist - try again when you have it")
            sys.exit(-1)
        elif a == 5:
            print("Please enter your choice:")
        else:
            print("ERROR")

    def test_setup_scli_neg(self):
        """
        Test for scli setup
        """
        self.pobj.sendline("1")
        set_up = self.pobj.expect(["Do you want to re-encrypt the dataset?","Pushed dataset","Skipping encrypt input data in standalone mode","Are you logged into the Sensoriant registry?",pexpect.EOF],timeout=120)
        self.assertTrue(set_up in [0,1,2,3])
        if set_up == 0:
            self.pobj.sendline('n')
            pushed = self.pobj.expect(["aborting re-encrypt ...","Success: Create Input DataSet",pexpect.EOF],timeout=120)
            self.assertEqual(pushed, 0)
            print("aborting re-encrypt ...")
        elif set_up == 1:
            self.assertEqual(pushed, 1)
            time.sleep(10)
            print("Success: Create Input DataSet")
        elif set_up == 2:
            print("Skipping encrypt input data in standalone mode")
        elif set_up == 3:
            print("Are you logged into the Sensoriant registry?")
            self.pobj.sendline('n')
            sens = self.pobj.expect(["Success: Create Input DataSet",pexpect.EOF],timeout==300)
            self.assertEqual(sens, 0)
            print("Success: Create Input DataSet")
            if sens == 0:
                time.sleep(10)

    def test_re_encrypt_neg(self):
        self.pobj.sendline("2")
        result = self.pobj.expect(["Do you want to re-encrypt the dataset?","Success: Create Input DataSet",pexpect.EOF],timeout=60)
        self.assertTrue(result in [0,1])
        if result == 0:
            self.pobj.sendline('n')
            r = self.pobj.expect(["aborting re-encrypt ...","Success: Create Input DataSet",pexpect.EOF],timeout=120)
            self.assertTrue(r == 0)
            if r == 0:
                print("aborting re-encrypt ...")
            elif r == 1:
                print("Success: Create Input DataSet")
            else:
                print("ERROR at step two")
                sys.exit(-1)
        elif result == 1:
            print("Skipping encrypt input data in standalone mode")


if __name__ == '__main__':
   # runner = unittest.TextTestRunner(verbosity=2,failfast=True)
   # runner.run(suite())
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestScliPositive("test_setup_scli"))
    test_suit.addTest(TestScliPositive("test_re_encrypt"))
    test_suit.addTest(TestScliPositive("test_switch_build"))
    test_suit.addTest(TestScliPositive("test_newbuild_genalgokey"))
    test_suit.addTest(TestScliNegative("test_setup_scli_neg"))
    test_suit.addTest(TestScliNegative("test_re_encrypt_neg"))
    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report").run(test_suit)
