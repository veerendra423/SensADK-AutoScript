#!/bin/bash

sudo apt install python-pip -y
pip install html-testRunner

#it will checks the pexpect module exists aren't if it is not there means it will install

test_pex=`pip show pexpect | grep Name`
echo "$test_pex"

if [ `echo $test_pex | tail -c 8` == "pexpect" ]; then
        echo "pexpect module available"
else
        echo "pexpect module not available installing"
        sudo apt install python-pip -y
        pip install pexpect
fi

#function to replace the variables in any file

replace_var()
{
        grep "^$1=" $3 >> /dev/null
        if [ $? -ne 0 ]; then
                echo $1=$2 >> $3
        else
                sed "\|^$1|s|=.*$|=$2|1" $3 > t
                mv t $3
        fi
}

#function to update adk.ini file
update_inifile()
{
	replace_var step_one y adk.ini
	replace_var step_two n adk.ini
	replace_var step_four y adk.ini
}
#function to test adk at clinet folder
run_adk_client()
{
	python2 adk_unittest_sub.py
	ret=$?
	if [ $ret -ne 0 ]; then
		exit 1
	fi
}
#funtion to test adk at sandbox
run_adk_sandbox()
{
	pushd ../sandbox/ >> /dev/null
	python2 adk_unittest_sandbox_sub.py
	ret=$?
        if [ $ret -ne 0 ]; then
                exit 1
        fi
	popd >> /dev/null
}
#function to update config file in standalone mode
stdmode_update_config()
{
	replace_var "export SCLI_STANDALONE" true config
        replace_var "export SBOX_STANDALONE" true ../sandbox/standalone.config
        replace_var "export SCLI_USE_REF" true config
        replace_var "export SCLI_FASTPUSH" true config
        replace_var "export SCLI_REMOVE_CACHED_IMAGE" true config
}
#function to update config file in api mode
apimode_update_config()
{
	replace_var "export SCLI_STANDALONE" false config
        replace_var "export SBOX_STANDALONE" false ../sandbox/standalone.config
        replace_var "export SCLI_USE_REF" true config
        replace_var "export SCLI_FASTPUSH" true config
        replace_var "export SCLI_REMOVE_CACHED_IMAGE" true config
}
exists=$(lsmod | grep -c nvidia)
if [ $exists -eq 6 ];
then
	echo "nvidia installed"
	#standalone mode testing part
	echo "unittesting in standalone mode on GPU machine in CPU-mode start">>report.txt
	stdmode_update_config
	replace_var "export SCLI_USE_GPU" false config
	run_adk_client
	#In standalone mode at sandbox side testing part
	run_adk_sandbox
	echo "unittesting in standalone mode on GPU machine in CPU-mode done">> report.txt
	
	#API mode testing part
	echo "unittesting in api mode on GPU machine in CPU-mode start">>report.txt
	source ./config
	ret=`curl -s -w "%{http_code}" --insecure -X GET "https://$SCLI_API_SERVER/secure_cloud_api/v1/secure_stream_platforms?limit=10&skip=0" -H  "accept: application/json"`
	if [ ! `echo $ret | tail -c 4` == "200" ]; then
        	echo API server not available
		exit 1
	else
        	apimode_update_config
		replace_var "export SCLI_USE_GPU" false config
		update_inifile
		run_adk_client
		echo "unittesting in api mode on GPU machine in CPU-mode done">>report.txt
	fi

        echo "unittesting in standalone mode on GPU machine in GPU-mode start">>report.txt
	stdmode_update_config
        replace_var "export SCLI_USE_GPU" true config
	run_adk_client
        #In standalone mode at sandbox side testing part
	run_adk_sandbox
	echo "unittesting in standalone mode on GPU machine in GPU-mode done">>report.txt
        
        #API mode testing part
        echo "unittesting in api mode on GPU machine in GPU-mode start">>report.txt
        source ./config
	ret=`curl -s -w "%{http_code}" --insecure -X GET "https://$SCLI_API_SERVER/secure_cloud_api/v1/secure_stream_platforms?limit=10&skip=0" -H  "accept: application/json"`
        if [ ! `echo $ret | tail -c 4` == "200" ]; then
                echo API server not available
		exit 1
        else
                apimode_update_config
                replace_var "export SCLI_USE_GPU" true config
		update_inifile
                run_adk_client
		echo "unittesting in api mode on GPU machine in GPU-mode done">>report.txt
        fi
	replace_var "export SCLI_USE_GPU" false config
	echo "end of GPU mode testing both api and std mode">>report.txt
	exit 1		
else
	echo "nvidia not installed this is not GPU_MACHINE"
fi

#standalone mode testing part

echo "unittesting in standalone mode with fast_push mode start" >> report.txt
stdmode_update_config
run_adk_client
#In standalone mode at sandbox side testing part
run_adk_sandbox
echo "unittesting in standalone mode with fastpush mode done" >>report.txt
#exit 1

#API mode testing part
echo "unittesting in api mode with fastpush mode start" >>report.txt
source ./config
ret=`curl -s -w "%{http_code}" --insecure -X GET "https://$SCLI_API_SERVER/secure_cloud_api/v1/secure_stream_platforms?limit=10&skip=0" -H  "accept: application/json"`
if [ ! `echo $ret | tail -c 4` == "200" ]; then
	echo API server not available
	exit 1
else
	apimode_update_config
	update_inifile
	run_adk_client
	echo "unittesting in api mode with fastpush mode done" >> report.txt
fi

#exit 1
#without fastpush mode
#standalone without fastpush mode and without reference image testing part
sudo rm -f image/sdata/refcpu.tar
echo "unittesting in standalone without fast push mode start" >>report.txt
replace_var "export SCLI_STANDALONE" true config
replace_var "export SBOX_STANDALONE" true ../sandbox/standalone.config
replace_var "export SCLI_USE_REF" false config
replace_var "export SCLI_FASTPUSH" false config
replace_var "export SCLI_REMOVE_CACHED_IMAGE" false config

run_adk_client
#In standalone mode at sandbox side testing part
run_adk_sandbox
echo "unittesting in standalone without fast push mode done">>report.txt

#API without fastpush mode and without reference image testing part
sudo rm -f image/sdata/refcpu.tar
echo "unittesting in api mode without fastpush mode start" >> report.txt
source ./config
ret=`curl -s -w "%{http_code}" --insecure -X GET "https://$SCLI_API_SERVER/secure_cloud_api/v1/secure_stream_platforms?limit=10&skip=0" -H  "accept: application/json"`
if [ ! `echo $ret | tail -c 4` == "200" ]; then
        echo API server not available
	exit 1
else
        replace_var "export SCLI_STANDALONE" false config
        replace_var "export SBOX_STANDALONE" false ../sandbox/standalone.config
	replace_var "export SCLI_USE_REF" false config
        replace_var "export SCLI_FASTPUSH" false config
        replace_var "export SCLI_REMOVE_CACHED_IMAGE" false config
        
	update_inifile
	run_adk_client
	echo "unittesting in api mode without fastpush mode done" >> report.txt
fi

replace_var "export SCLI_USE_REF" true config
replace_var "export SCLI_FASTPUSH" true config
replace_var "export SCLI_REMOVE_CACHED_IMAGE" true config
