import re
import json
import errno
import subprocess
import HtmlTestRunner
import unittest
import pexpect
import sys
import time
import os
import os.path
import getpass
#import ConfigParser


class TestScliPositive(unittest.TestCase):

    def setUp(self):
        print ("setup")
        psource = subprocess.call(['bash', '-c', 'source ./safectl.azure-defaults.env'])
        if psource == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_setup_scli(self):
        ps = 0 
        if ps == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_clear_session(self):
        p0 = subprocess.call(['bash', '-c', 'source scripts/0-clear_session.sh'])
        if p0 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)


    def test_safelet_provider_encrypt(self):
        p1 = subprocess.call(['bash', '-c', 'source scripts/1-safelet_provider_encrypt.sh'])
        if p1 == 0:
            print("pass")
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file1 = user+'/safelet-created.json'
            with open(file1, 'r') as f:
                distros_dict = json.load(f)

            for distro in distros_dict:
                data=distro['keyid']
                print(data)
        else:
            print("Fail")
            sys.exit(-1)

    def test_safelet_provider_encrypt_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file1 = user+'/safelet-created.json'
            with open(file1, 'r') as f:
                distros_dict = json.load(f)

            for distro in distros_dict:
                data=distro['keyid']
                print(data)

            fileframe = user+'/owner_keys/'+data+'/safelet_enclave_key.txt'
            print(fileframe)

            if(os.path.exists(fileframe)):
                print("enclave key File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_encrypt_owner_keys(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file1 = user+'/safelet-created.json'
            with open(file1, 'r') as f:
                distros_dict = json.load(f)

            for distro in distros_dict:
                data=distro['keyid']
                print(data)
                print(user+'/owner_keys/'+data)
            fileframe = user+'/owner_keys/'+data+'/safelet_enclave_tag_key.txt'
            print(fileframe)
            if(os.path.exists(fileframe)):
                print("enclave_tag File Exists!!")        
            else:            
                print("File does not exists!!")
                sys.exit(-1)

    def test_safelet_provider_encrypt_owner_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file1 = user+'/safelet-created.json'
            with open(file1, 'r') as f:

                distros_dict = json.load(f)

            for distro in distros_dict:
                data=distro['keyid']
                print(data)
                print(user+'/owner_keys/'+data)
            owner = data+'_safelet_enclave.json'
            fileframe = user+'/owner_keys/'+data+'/'+owner
            print(fileframe)

            if(os.path.exists(fileframe)):
                print("owner File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_encrypt_sign_private(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file1 = user+'/signing-key-pair-safelet/private-key.pem'

            if(os.path.exists(file1)):
                print("private key File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_encrypt_sign_public(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file2 = user+'/signing-key-pair-safelet/public-key.pem'

            if(os.path.exists(file2)):
                print("public-key File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_encrypt_session(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file2 = user+'/session.yaml'

            if(os.path.exists(file2)):
                print("session.yaml File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_encrypt_app(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            username = getpass.getuser()
            print(username)
            file2 = 'ghelloapp_safelet'
            file3 = user+file2

            if(os.path.exists(file3)):
                print("safelet directory Exists!!")
            else:
                print("File does not exists!!")

    def test_data_provider_encrypt(self):
        p2 = subprocess.call(['bash', '-c', 'source scripts/2-data_provider_encrypt.sh'])
        if p2 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_data_provider_encrypt_datasetjson(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file2 = user+'/dataset-created.json'

            if(os.path.exists(file2)):
                print("dataset-created File Exists!!")
            else:
                print("File does not exists!!")

    def test_data_provider_encrypt_datasetinput(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            username = getpass.getuser()
            print(username)
            file2 = 'ghelloapp_input'

            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file3 = user+file2+'/current_ds.json'

            if(os.path.exists(file3)):
                print("current_ds.json File Exists!!")
            else:
                print("File does not exists!!")

    def test_data_provider_encrypt_defaultownerinput(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            username = getpass.getuser()
            print(username)
            file2 = 'ghelloapp_input'

            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp/"+file2+"/default_owner_key.json"
            print(user)

            if(os.path.exists(user)):
                print("default ownerkey File Exists!!")
            else:
                print("File does not exists!!")


    def test_output_consumer_encrypt(self):
        p3 = subprocess.call(['bash', '-c', 'source scripts/3-output_consumer_encrypt.sh'])
        if p3 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_output_consumer_datasetoutput(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            username = getpass.getuser()
            print(username)
            file2 = 'ghelloapp_output'

            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)
            file3 = user+file2+"/decoded_dec_key.txt"

            if(os.path.exists(file3)):
                print("decoded_dec_key.txt File Exists!!")
            else:
                print("File does not exists!!")

    def test_safelet_provider_secret(self):
        p4 = subprocess.call(['bash', '-c', 'source scripts/4-safelet_provider_secret.sh'])
        if p4 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_safelet_provider_secret_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            file3 = user+"/secret-safelet.json"

            if(os.path.exists(file3)):
                print("secret-safelet.json File Exists!!")
            else:
                print("File does not exists!!")

    def test_data_provider_secret(self):
        p5 = subprocess.call(['bash', '-c', 'source scripts/5-data_provider_secret.sh'])
        if p5 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_data_provider_secret_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            file3 = user+"/secret-dataset.json"

            if(os.path.exists(file3)):
                print("secret-dataset.json File Exists!!")
            else:
                print("File does not exists!!")

    def test_output_consumer_secret(self):
        p6 = subprocess.call(['bash', '-c', 'source scripts/6-output_consumer_secret.sh'])
        if p6 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_output_consumer_secret_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            file3 = user+"/secret-output.json"

            if(os.path.exists(file3)):
                print("secret-output.json File Exists!!")
            else:
                print("File does not exists!!")

    def test_safestream_operator(self):
        p7 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
        if p7 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_safestream_operator_file(self):
            homedir = os.environ['HOME']
            user = homedir+"/.safectl/ghelloapp"
            print(user)

            file3 = user+"/safestream-created.json"

            if(os.path.exists(file3)):
                print("safestream-created.json File Exists!!")
            else:
                print("File does not exists!!")


    def test_wait_for_safestream(self):
        p8 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
        if p8 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_output_consumer_pull(self):
        p9 = subprocess.call(['bash', '-c', 'source scripts/9-output_consumer_pull.sh'])
        if p9 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)

    def test_group_1_clear_prior_session(self):
        p10 = subprocess.call(['bash', '-c', 'source scripts/group-1-clear-prior-session.sh'])
        if p10 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_group_2_encrypt_and_push(self):
        p11 = subprocess.call(['bash', '-c', 'source scripts/group-2-encrypt-and-push.sh'])
        if p11 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_group_3_generate_secrets(self):
        p12 = subprocess.call(['bash', '-c', 'source scripts/group-3-generate-secrets.sh'])
        if p12 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_group_4_run_check_safestream(self):
        p12 = subprocess.call(['bash', '-c', 'source scripts/group-4-run-check-safestream.sh'])
        if p12 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_group_5_pull_and_decrypt(self):
        p12 = subprocess.call(['bash', '-c', 'source scripts/group-5-pull-and-decrypt.sh'])
        if p12 == 0:
            print("pass")
        else:
            print("Fail")
            sys.exit(-1)
    def test_config_safelet_and_stream(self):
        p13 = subprocess.call(['bash', '-c', 'source scripts/1-safelet_provider_encrypt.sh'])
        if p13 == 0:
            print("safelet provider passed")
            p14 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p14 == 0:
                print("stream started")
                p15 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p15 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)

    def test_config_dataprovider_and_stream(self):
        p16 = subprocess.call(['bash', '-c', 'source scripts/2-data_provider_encrypt.sh'])
        if p16 == 0:
            print("data provider passed")
            p17 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p17 == 0:
                print("stream started")
                p18 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p18 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_config_output_consumer_encrypt_and_stream(self):
        p19 = subprocess.call(['bash', '-c', 'source scripts/3-output_consumer_encrypt.sh'])
        if p19 == 0:
            print("output consumer encrypt passed")
            p20 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p20 == 0:
                print("stream started")
                p21 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p21 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)

    def test_config_safelet_provider_secret_and_stream(self):
        p22 = subprocess.call(['bash', '-c', 'source scripts/4-safelet_provider_secret.sh'])
        if p22 == 0:
            print("config_safelet_provider_secret passed")
            p23 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p23 == 0:
                print("stream started")
                p24 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p24 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_config_dataprovider_secret_and_stream(self):
        p25 = subprocess.call(['bash', '-c', 'source scripts/5-data_provider_secret.sh'])
        if p25 == 0:
            print("dataprovider secret passed")
            p26 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p26 == 0:
                print("stream started")
                p27 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p27 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_config_output_consumer_and_stream(self):
        p28 = subprocess.call(['bash', '-c', 'source scripts/6-output_consumer_secret.sh'])
        if p28 == 0:
            print("output consumer passed")
            p29 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p29 == 0:
                print("stream started")
                p30 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                if p30 == 0:
                    print("safestream success")
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_group_config_2_encrypt_push_and_stream(self):
        p31 = subprocess.call(['bash', '-c', 'source scripts/group-2-encrypt-and-push.sh'])
        if p31 == 0:
            print("output consumer passed")
            p32 = subprocess.call(['bash', '-c', 'source scripts/group-4-run-check-safestream.sh'])
            if p32 == 0:
                print("stream success")
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_group_config_3_generate_secrets_and_stream(self):
        p33 = subprocess.call(['bash', '-c', 'source scripts/group-3-generate-secrets.sh'])
        if p33 == 0:
            print("output consumer passed")
            p34 = subprocess.call(['bash', '-c', 'source scripts/group-4-run-check-safestream.sh'])
            if p34 == 0:
                print("stream success")
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_multipipeline_config_safeletprovider_and_stream(self):
        p35 = subprocess.call(['bash', '-c', 'source scripts/1-safelet_provider_encrypt.sh'])
        if p35 == 0:
            print("safelet provider passed")
            p36 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p36 == 0:
                print("safestream one started")
                p37 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if p37 == 0:
                    print("safestream two started")
                    p38 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if p38 == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)
                    
                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)

    def test_multipipeline_config_dataprovider_and_stream(self):
        p39 = subprocess.call(['bash', '-c', 'source scripts/2-data_provider_encrypt.sh'])
        if p39 == 0:
            print("data provider passed")
            p40 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p40 == 0:
                print("safestream one started")
                p41 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if p41 == 0:
                    print("safestream two started")
                    p42 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if p42 == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)

                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)

    def test_multipipeline_config_output_consumer_and_stream(self):
        p43 = subprocess.call(['bash', '-c', 'source scripts/3-output_consumer_encrypt.sh'])
        if p43 == 0:
            print("output consumer encrypt passed")
            p44 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p44 == 0:
                print("safestream one started")
                p45 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if p45 == 0:
                    print("safestream two started")
                    p46 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if p46 == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)

                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)

    def test_multipipeline_config_safelet_provider_secret_and_stream(self):
        ps = subprocess.call(['bash', '-c', 'source scripts/4-safelet_provider_secret.sh'])
        if ps == 0:
            print("safelet_provider_secret passed")
            pt = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if pt == 0:
                print("safestream one started")
                pv = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if pv == 0:
                    print("safestream two started")
                    pr = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if pr == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)

                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)


    def test_multipipeline_config_data_provider_secret_and_stream(self):
        p47 = subprocess.call(['bash', '-c', 'source scripts/5-data_provider_secret.sh'])
        if p47 == 0:
            print("data_provider_secret  passed")
            p48 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p48 == 0:
                print("safestream one started")
                p49 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if p49 == 0:
                    print("safestream two started")
                    p50 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if p50 == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)

                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)
    def test_multipipeline_config_output_consumer_secret_and_stream(self):
        p51 = subprocess.call(['bash', '-c', 'source scripts/6-output_consumer_secret.sh '])
        if p51 == 0:
            print("output_consumer_secret passed")
            p52 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
            if p52 == 0:
                print("safestream one started")
                p53 = subprocess.call(['bash', '-c', 'source scripts/7-safestream_operator.sh'])
                if p53 == 0:
                    print("safestream two started")
                    p54 = subprocess.call(['bash', '-c', 'source scripts/8-wait_for_safestream.sh'])
                    if p54 == 0:
                        print("safestream success")
                    else:
                        print("Fail")
                        sys.exit(-1)

                else:
                    print("Fail")
                    sys.exit(-1)
            else:
                print("Fail")
                sys.exit(-1)

        else:
            print("Fail")
            sys.exit(-1)



if __name__ == '__main__':
    test_suit = unittest.TestSuite()
    test_suit.addTest(TestScliPositive("test_clear_session"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_file"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_owner_keys"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_owner_file"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_sign_private"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_sign_public"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_session"))
    test_suit.addTest(TestScliPositive("test_safelet_provider_encrypt_app"))
    test_suit.addTest(TestScliPositive("test_data_provider_encrypt"))
    test_suit.addTest(TestScliPositive("test_data_provider_encrypt_datasetjson"))
    test_suit.addTest(TestScliPositive("test_data_provider_encrypt_datasetinput"))
    test_suit.addTest(TestScliPositive("test_data_provider_encrypt_defaultownerinput"))
    test_suit.addTest(TestScliPositive("test_output_consumer_encrypt"))
    test_suit.addTest(TestScliPositive("test_output_consumer_datasetoutput"))
    test_suit.addTest(TestScliPositive('test_safelet_provider_secret'))
    test_suit.addTest(TestScliPositive('test_safelet_provider_secret_file'))
    test_suit.addTest(TestScliPositive('test_data_provider_secret'))
    test_suit.addTest(TestScliPositive('test_data_provider_secret_file'))
    test_suit.addTest(TestScliPositive('test_output_consumer_secret'))
    test_suit.addTest(TestScliPositive('test_output_consumer_secret_file'))
    test_suit.addTest(TestScliPositive('test_safestream_operator'))
    test_suit.addTest(TestScliPositive('test_safestream_operator_file'))
    test_suit.addTest(TestScliPositive('test_wait_for_safestream'))
    test_suit.addTest(TestScliPositive('test_output_consumer_pull'))
    test_suit.addTest(TestScliPositive('test_group_1_clear_prior_session'))
    test_suit.addTest(TestScliPositive('test_group_2_encrypt_and_push'))
    test_suit.addTest(TestScliPositive('test_group_3_generate_secrets'))
    test_suit.addTest(TestScliPositive('test_group_4_run_check_safestream'))
    test_suit.addTest(TestScliPositive('test_group_5_pull_and_decrypt'))
    test_suit.addTest(TestScliPositive('test_config_safelet_and_stream'))
    test_suit.addTest(TestScliPositive('test_config_dataprovider_and_stream'))
    test_suit.addTest(TestScliPositive('test_config_output_consumer_encrypt_and_stream'))
    test_suit.addTest(TestScliPositive('test_config_safelet_provider_secret_and_stream'))
    test_suit.addTest(TestScliPositive('test_config_dataprovider_secret_and_stream'))
    test_suit.addTest(TestScliPositive('test_config_output_consumer_and_stream'))
    test_suit.addTest(TestScliPositive('test_group_config_2_encrypt_push_and_stream'))
    test_suit.addTest(TestScliPositive('test_group_config_3_generate_secrets_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_safeletprovider_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_dataprovider_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_output_consumer_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_safelet_provider_secret_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_data_provider_secret_and_stream'))
    test_suit.addTest(TestScliPositive('test_multipipeline_config_output_consumer_secret_and_stream'))
    smoke_tests = unittest.TestSuite(test_suit)
    h = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_name="adk_test_report").run(test_suit)
