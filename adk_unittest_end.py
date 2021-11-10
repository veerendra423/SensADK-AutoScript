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
log = cfg.get('adk', 'log')
print(log)

cli = os.environ['CURRENT_BUILD_SCLI']
print(cli)

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

    def test_runimage_locally(self):
        self.pobj.sendline("5")
        run_image = self.pobj.expect(['"loss"',"Not Done","not supported with SCLI_REMOVE_CACHED_IMAGE=true",pexpect.EOF],timeout=90)
        time.sleep(5)
        self.assertTrue(run_image in [0,2])
        if run_image == 0:
            print("Save model")
        elif run_image == 1:
            print("Run_Image_Locally: failed")
        elif run_image == 2:
            print("not supported with SCLI_REMOVE_CACHED_IMAGE=true")
        else:
            print("ERROR at Run Image locally")
            sys.exit(-1)

    def test_encrypt_sign_image(self):
        self.pobj.sendline("6")
        encrypt_sign = self.pobj.expect(['"status": true',"file already exists!",pexpect.EOF],timeout=240)
        self.assertTrue(encrypt_sign in [0,1])
        print("encrypt and sign done")
        if encrypt_sign == 0:
            time.sleep(5)
        elif encrypt_sign == 1:
            print("file already exists!")
        else:
            print("ERROR at step-6")
            sys.exit(-1)

    def test_build_dir_check(self):
        path = 'image/sdata/'
        x = ''
        with open('.build-env') as f:
            for line in f:
                if 'CURRENT_BUILD_SCLI' in line:
                    fields = line.strip().split("=")
                    x = fields[1]
                    print(x)
        test_path = path+x
        dir_check = os.path.isdir(test_path)
        print(dir_check)
        self.assertEqual(dir_check,True)
        print("current build number available")

    def test_measurment_textfile(self):
        path = os.getenv("SCLI_MEAS_FILE")
        print(path)
        file_check = os.path.exists(path)
        print(file_check)
        self.assertEqual(file_check,True)
        print("measuremnt file exits")

    def test_enc_priv_pemfile(self):
        path = os.getenv("SCLI_IPK_FILE")
        print(path)
        file_check = os.path.exists(path)
        print(file_check)
        self.assertEqual(file_check,True)
        print("encrypted private pem file available")

    def test_enc_tarfile(self):
        path = os.getenv("SCLI_IMAGE_TAR_FILE")
        print(path)
        file_check = os.path.exists(path)
        print(file_check)
        self.assertEqual(file_check,True)
        print("encrypted tar file available")

    def test_submit_imagetar(self):
        self.pobj.sendline("7")
        submit = self.pobj.expect(["Success: Submit Algorithm","Done..","Nothing to import in FASTPUSH mode",pexpect.EOF],timeout=300)
        self.assertTrue(submit in [0,1,2])
        if submit == 0:
            print("Success: Submit Algorithm")
        elif submit == 1:
            print("Std mode Success: Submit Algorithm")
        elif submit == 2:
            print("Nothing to import in FASTPUSH mode")
        else:
            print("ERROR at step-7")
            sys.exit(-1)

    def test_create_platform(self):
        self.pobj.sendline("8")
        create = self.pobj.expect(["Success: Get Platform","Failed: Get Platform","Will use default platform key",pexpect.EOF],timeout=90)
        self.assertTrue(create in [0,2])
        if create == 0:
            print("Success: Get Platform")
        elif create == 1:
            print("Failed: Get Platform")
            print("Create_Platform: failed")
            sys.exit(-1)
        elif create == 2:
            time.sleep(5)
            print("Will use default platform key")
        else:
            print("ERROR at step-8")
            sys.exit(-1)

    def test_ssp_jsonfile(self):
        path = os.getenv('SCLI_ALGO_DIR')
        x = ''
        with open('.build-env') as f:
            for line in f:
                if 'CURRENT_BUILD_SCLI' in line:
                    fields = line.strip().split("=")
                    x = fields[1]
                    print(x)
        path = path+'/'+x+'/ssp.json'
        print(path)
        ssp = os.path.exists(path)
        print(ssp)
        self.assertTrue(ssp == True)
        print("ssp.json file available")

    def test_create_and_uplodedatasetkeys(self):
        self.pobj.sendline("9")
        upload = self.pobj.expect(['"status": true',"Failed: Push DataSet Key","In Standalone mode ... skipping Push DataSet Keys ...",pexpect.EOF],timeout=90)
        time.sleep(10)
        self.assertTrue(upload in [0,2])
        if upload == 0:
            print("Success: Push DataSet Key")
        elif upload == 1:
            print("Failed: Push DataSet Key")
            sys.exit(-1)
        elif upload == 2:
            print("Success: Push DataSet Key")
        else:
            print("ERROR at step-9")
            sys.exit(-1)

    def test_create_and_submitpilpeline(self):
        self.pobj.sendline("10")
        submit_pipe = self.pobj.expect(["Success: Create Pipeline","Failed: Get DataSet Key","Failed: Create Pipeline",pexpect.EOF],timeout=90)
        #self.assertEqual(submit_pipe,0)
        if submit_pipe == 0:
            print("Success: Create Pipeline")
            time.sleep(5)
        elif submit_pipe == 1:
            print("Create_and_Submit_Pipeline: failed")
          #  sys.exit(-1)
        elif submit_pipe == 2:
            print("Create_and_Submit_Pipeline: failed")
         #   sys.exit(-1)
        else:
            print("ERROR at step-10")
            sys.exit(-1)

    def test_create_and_submitpilpeline_second(self):
        self.pobj.sendline("10")
        submit_pipe = self.pobj.expect(["Success: Create Pipeline","Failed: Get DataSet Key","Failed: Create Pipeline",pexpect.EOF],timeout=90)
        self.assertEqual(submit_pipe,0)
        if submit_pipe == 0:
            print("Success: Create Pipeline")
            time.sleep(5)
        elif submit_pipe == 1:
            print("Create_and_Submit_Pipeline: failed")
            sys.exit(-1)
        elif submit_pipe == 2:
            print("Create_and_Submit_Pipeline: failed")
            sys.exit(-1)
        else:
            print("ERROR at step-10")
            sys.exit(-1)


    def test_algo_outputfile(self):
        path = os.getenv('SCLI_ALGO_DIR')
        x = ''
        with open('.build-env') as f:
            for line in f:
                if 'CURRENT_BUILD_SCLI' in line:
                    fields = line.strip().split("=")
                    x = fields[1]
                    print(x)
        path = path+'/'+x+'/'
        print(path)
        test_list = ['algorithm.decryptionKeys.enclave.decryptionKey','algorithm.decryptionKeys.enclave.decryptionKey-eb','output.encryptionkey.symmetrickey','output.encryptionkey.symmetrickey-eb','pipeline.json']
        for i in test_list:
            path_test=path+i
            print(os.path.exists(path_test))
            x = os.path.exists(path_test)
            self.assertTrue(x == True)
            print("algo output files available")

    def test_enc_priv_pem_ekfile(self):
        ek = os.getenv('SCLI_EPK_FILE')
        print(ek)
        testek = os.path.exists(ek)
        print(testek)
        self.assertTrue(testek == True)
        print("encrypted private key(EPK) file available")

    def test_start_pipeline(self):
        self.pobj.sendline("11")
        start_pipe = self.pobj.expect(["Success: Start Pipeline","In Standalone mode ... feature not available...","Failed: Start Pipeline",pexpect.EOF],timeout=600)
        self.assertTrue(start_pipe in [0,1,2])
        if start_pipe == 0:
            print("Success: Start Pipeline")
            time.sleep(10)
        elif start_pipe == 1:
            print("feature not available")
        elif start_pipe == 2:
            print("Failed: Start Pipeline")
            sys.exit(-1)
        else:
            print("ERROR at step-11")
            sys.exit(-1)

    def test_ftech_and_decryptoutput(self):
        self.pobj.sendline("12")
        Decrypt = self.pobj.expect(['"loss"',"In Standalone mode ... nothing to pull and decrypt ...",pexpect.EOF],timeout=60)
        self.assertTrue(Decrypt in [0,1])
        if Decrypt == 0:
            time.sleep(15)
            print("Decrypted test_metrics file")
        elif Decrypt == 1:
            print("feature not available")
        else:
            print("ERROR at step-12")
            sys.exit(-1)


if __name__ == '__main__':
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(suite))
    #runner = unittest.TextTestRunner(verbosity=2,failfast=True)
    #runner.run(suite())
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestScliPositive('test_runimage_locally'))
    test_suit.addTest(TestScliPositive('test_encrypt_sign_image'))
    test_suit.addTest(TestScliPositive('test_build_dir_check'))
    test_suit.addTest(TestScliPositive('test_measurment_textfile'))
    test_suit.addTest(TestScliPositive('test_enc_priv_pemfile'))
    #suite.addTest(TestScliPositive('test_enc_tarfile'))
    test_suit.addTest(TestScliPositive('test_submit_imagetar'))
    test_suit.addTest(TestScliPositive('test_create_platform'))
    test_suit.addTest(TestScliPositive('test_ssp_jsonfile'))
    test_suit.addTest(TestScliPositive('test_create_and_uplodedatasetkeys'))
    test_suit.addTest(TestScliPositive('test_create_and_submitpilpeline'))
    test_suit.addTest(TestScliPositive('test_create_and_submitpilpeline_second'))
    test_suit.addTest(TestScliPositive('test_algo_outputfile'))
    test_suit.addTest(TestScliPositive('test_enc_priv_pem_ekfile'))
    test_suit.addTest(TestScliPositive('test_start_pipeline'))
    test_suit.addTest(TestScliPositive('test_ftech_and_decryptoutput'))
    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report2").run(test_suit)
