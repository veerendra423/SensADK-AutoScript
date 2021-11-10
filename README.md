#To run the adk automation script

copy the following files into the adk/client/ folder, wherever you are running adk,

1.adk.ini
2.adk_unittest.sh
3.adk_unittest_start.py
4.adk_unittest_end.py

copy the following file into the adk/sandbox/ folder, wherever you are running adk,

1.adk_unittest_sandbox.py

#To run the adk automation script.
note:- Make sure you need to update the config file ip server and path to the adk.
#you need to run the script inside the client folder.

./adk_unittest.sh


adktest.py and and autotest.sh file used for the safectl testing.
safectl-config file used for the parameters.
we need to provide the .env file in adktest.py
we need to provide the .env file for safectl-config.
