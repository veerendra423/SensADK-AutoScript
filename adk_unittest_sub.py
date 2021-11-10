import re
import errno
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
        print ("setup")
    def test_setup_scli(self):
        p1 = subprocess.call(['bash', '-c', 'source scli-menu.sh && setup_scli'])
        if p1 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_re_encrypt(self):
        p2 = subprocess.call(['bash', '-c', 'source scli-menu.sh && echo "n" | re_create_dataset'])
        if p2 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)


    def test_switch_build(self):
        p3 = subprocess.call(['bash', '-c', 'source scli-menu.sh && echo "q" | switch_build'])
        if p3 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_newbuild_genalgokey(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p4 = subprocess.call(['bash', '-c', 'source scli-menu.sh && build_container_image'])
        if p4 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_runimage_locally(self):
        p5 = subprocess.call(['bash', '-c', 'source scli-menu.sh && run_image_locally'])
        if p5 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_encrypt_sign_image(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p6 = subprocess.call(['bash', '-c', 'source scli-menu.sh && run_esig'])
        if p6 == 0:
            print("pass")
        else:
            print("Fail")
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
        pc = subprocess.call(['bash', '-c', 'source ./.build-env && source config && echo "$SCLI_MEAS_FILE" >> file.txt'])
        a_file = open("file.txt")
        lines_to_read = [0, 1]
        for position, line in enumerate(a_file):
            if position in lines_to_read:
                #print(line)
                file_check = os.path.exists(line.strip())
                self.assertEqual(file_check,True)
                print("measuremnt file exits")
        pr = subprocess.call(['bash', '-c', 'rm -f file.txt'])

    def test_enc_priv_pemfile(self):
        pc = subprocess.call(['bash', '-c', 'source ./.build-env && source config && echo "$SCLI_IPK_FILE" >> file.txt'])
        a_file = open("file.txt")
        lines_to_read = [0, 1]
        for position, line in enumerate(a_file):
            if position in lines_to_read:
                #print(line)
                file_check = os.path.exists(line.strip())
                self.assertEqual(file_check,True)
                print("encrypted priv file exits")
        pr = subprocess.call(['bash', '-c', 'rm -f file.txt'])

    def test_submit_imagetar(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p7 = subprocess.call(['bash', '-c', 'source scli-menu.sh && run_import_tar'])
        if p7 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_create_platform(self):
        p8 = subprocess.call(['bash', '-c', 'source scli-menu.sh && create_platform'])
        if p8 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_ssp_jsonfile(self):
        pc = subprocess.call(['bash', '-c', 'source config && echo "$SCLI_ALGO_DIR" >> file.txt'])
        x = ''
        with open('.build-env') as f:
            for line in f:
                if 'CURRENT_BUILD_SCLI' in line:
                    fields = line.strip().split("=")
                    x = fields[1]
                 #   print(x)

        a_file = open("file.txt")
        lines_to_read = [0, 1]
        for position, line in enumerate(a_file):
            if position in lines_to_read:
                #print(line)
                file_check = os.path.exists(line.strip())
                path = line.strip()+'/'+x+'/ssp.json'
                #print(path)
                ssp = os.path.exists(path.strip())
                #print(ssp)
                self.assertTrue(ssp == True)
                print("ssp.json file available")

        pr = subprocess.call(['bash', '-c', 'rm -f file.txt'])

    def test_create_and_uplodedatasetkeys(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p9 = subprocess.call(['bash', '-c', 'source scli-menu.sh && push_dataset_keys'])
        if p9 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_create_and_submitpilpeline(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p10 = subprocess.call(['bash', '-c', 'source scli-menu.sh && create_pipeline >> pipe.log'])
        if p10 != 0:
            pattern = "Failed: Create Pipeline"
            file = open("pipe.log", "r")
            for line in file:
                if re.search(pattern, line):
                    p10 = 1
            file.close()
            print("Fail")
            sys.exit(-1)

        if p10 == 0:
            print("pass")

        pr = subprocess.call(['bash', '-c', 'rm -f pipe.log'])

    def test_algo_outputfile(self):
        pc = subprocess.call(['bash', '-c', 'source config && echo "$SCLI_ALGO_DIR" >> file.txt'])
        x = ''
        with open('.build-env') as f:
            for line in f:
                if 'CURRENT_BUILD_SCLI' in line:
                    fields = line.strip().split("=")
                    x = fields[1]
                 #   print(x)

        a_file = open("file.txt")
        lines_to_read = [0, 1]
        for position, line in enumerate(a_file):
            if position in lines_to_read:
                #print(line)
                file_check = os.path.exists(line.strip())
                path = line.strip()+'/'+x+'/'

        test_list = ['algorithm.decryptionKeys.enclave.decryptionKey','algorithm.decryptionKeys.enclave.decryptionKey-eb','output.encryptionkey.symmetrickey','output.encryptionkey.symmetrickey-eb','pipeline.json']
        for i in test_list:
            path_test=path+i
            print(os.path.exists(path_test.strip()))
            x = os.path.exists(path_test.strip())
            self.assertTrue(x == True)
            print("algo output files available")
        
        pr = subprocess.call(['bash', '-c', 'rm -f file.txt'])

    def test_enc_priv_pem_ekfile(self):
        pc = subprocess.call(['bash', '-c', 'source ./.build-env && source config && echo "$SCLI_EPK_FILE" >> file.txt'])
        a_file = open("file.txt")
        lines_to_read = [0, 1]
        for position, line in enumerate(a_file):
            if position in lines_to_read:
                #print(line)
                file_check = os.path.exists(line.strip())
        self.assertTrue(file_check == True)
        print("encrypted private key(EPK) file available")

        pr = subprocess.call(['bash', '-c', 'rm -f file.txt'])
    
    def test_start_pipeline(self):
        pcon = subprocess.call(['bash', '-c', 'source config && source .build-env'])
        p11 = subprocess.call(['bash', '-c', 'source scli-menu.sh && start_pipeline >> pipe.log'])
        pattern = "Failed: Start Pipeline"
        file = open("pipe.log", "r")
        for line in file:
            if re.search(pattern, line):
                p11 = 1
        file.close()

        if p11 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

        pr = subprocess.call(['bash', '-c', 'rm -f pipe.log'])

    def test_ftech_and_decryptoutput(self):
        p12 = subprocess.call(['bash', '-c', 'source scli-menu.sh && pull_decrypt_output >> pipe.log'])
        pattern = "Try again after you create and submit pipeline ..."
        file = open("pipe.log", "r")
        for line in file:
            if re.search(pattern, line):
                p12 = 1
        file.close()
        if p12 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

if __name__ == '__main__':
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestScliPositive("test_setup_scli"))
    test_suit.addTest(TestScliPositive("test_re_encrypt"))
    test_suit.addTest(TestScliPositive("test_switch_build"))
    test_suit.addTest(TestScliPositive("test_newbuild_genalgokey"))
    test_suit.addTest(TestScliPositive('test_runimage_locally'))
    test_suit.addTest(TestScliPositive('test_encrypt_sign_image'))
    test_suit.addTest(TestScliPositive('test_build_dir_check'))
    test_suit.addTest(TestScliPositive('test_measurment_textfile'))
    test_suit.addTest(TestScliPositive('test_enc_priv_pemfile'))
    test_suit.addTest(TestScliPositive('test_submit_imagetar'))
    test_suit.addTest(TestScliPositive('test_create_platform'))
    test_suit.addTest(TestScliPositive('test_ssp_jsonfile'))
    test_suit.addTest(TestScliPositive('test_create_and_uplodedatasetkeys'))
    test_suit.addTest(TestScliPositive('test_create_and_submitpilpeline'))
    test_suit.addTest(TestScliPositive('test_algo_outputfile'))
    test_suit.addTest(TestScliPositive('test_enc_priv_pem_ekfile'))
    test_suit.addTest(TestScliPositive('test_start_pipeline'))
    test_suit.addTest(TestScliPositive('test_ftech_and_decryptoutput'))
    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report").run(test_suit)
