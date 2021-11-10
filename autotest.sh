#!/bin/bash
a=0
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


source ./safectl-config
source ./$SAFECTLENV


./scripts/all-groups.sh

ret=$?
if [ $ret -ne 0 ]; then
	echo "failed"
        exit 1
else
	echo "all groups passed"
fi

safestream_func()
{
./scripts/7-safestream_operator.sh
ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "started stream"
fi

./scripts/8-wait_for_safestream.sh
ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "safestream sucsess"
fi
}

multi_safestream_func()
{
./scripts/7-safestream_operator.sh
ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "first safestream started"
fi

./scripts/7-safestream_operator.sh
ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "second safestream started"
fi

./scripts/8-wait_for_safestream.sh
ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "safestream sucsess"
fi
}


group_safestream()
{
./scripts/group-4-run-check-safestream.sh

ret=$?
if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
else
        echo "group-4-run-check-safestream success"
fi
}


if [ $SINGLEPIPELINE == true ];
then
        ./scripts/1-safelet_provider_encrypt.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "safelet_provider_encrypt success"
        fi
        
        safestream_func
        
        ./scripts/2-data_provider_encrypt.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "data_provider_encrypt success"
        fi
        
        safestream_func
        
        ./scripts/3-output_consumer_encrypt.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_encrypt success"
        fi
        
        safestream_func
        
        ./scripts/4-safelet_provider_secret.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "safelet_provider_secret success"
        fi
        
        safestream_func
        
        ./scripts/5-data_provider_secret.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "data_provider_secret success"
        fi
        
        safestream_func
        
        ./scripts/6-output_consumer_secret.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_secret success"
        fi
        
        safestream_func
        
        ./scripts/9-output_consumer_pull.sh
        
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_pull success"
        fi
        
        ./scripts/group-2-encrypt-and-push.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-2-encrypt-and-push success"
        fi
        
        group_safestream
        
        ./scripts/group-3-generate-secrets.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-3-generate-secrets success"
        fi
        
        group_safestream
        
        ./scripts/group-5-pull-and-decrypt.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-5-pull-and-decrypt success"
        fi
	echo "single pipeline done"
fi


if [ $MULTIPIPELINE == true ];
then
        ./scripts/1-safelet_provider_encrypt.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "safelet_provider_encrypt success"
        fi

        multi_safestream_func

        ./scripts/2-data_provider_encrypt.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "data_provider_encrypt success"
        fi

        multi_safestream_func

        ./scripts/3-output_consumer_encrypt.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_encrypt success"
        fi

        multi_safestream_func

        ./scripts/4-safelet_provider_secret.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "safelet_provider_secret success"
        fi

        multi_safestream_func

        ./scripts/5-data_provider_secret.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "data_provider_secret success"
        fi

        multi_safestream_func

        ./scripts/6-output_consumer_secret.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_secret success"
        fi

        multi_safestream_func

        ./scripts/9-output_consumer_pull.sh

        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "output_consumer_pull success"
        fi

        ./scripts/group-2-encrypt-and-push.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-2-encrypt-and-push success"
        fi

        multi_safestream_func

        ./scripts/group-3-generate-secrets.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-3-generate-secrets success"
        fi

        multi_safestream_func

        ./scripts/group-5-pull-and-decrypt.sh
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "failed"
                exit 1
        else
                echo "group-5-pull-and-decrypt success"
        fi
	echo "multi pipeline done"
fi


if [ $LOADTEST == true ];
then
	while [ $a -lt 1000 ]
	do
		./scripts/7-safestream_operator.sh
		ret=$?
		if [ $ret -ne 0 ]; 
		then
			echo "failed"
			exit 1
		else
		       	echo "started stream"
		fi
		sleep 10
		./scripts/7-safestream_operator.sh
		ret=$?
		if [ $ret -ne 0 ]; 
		then
			echo "failed"
			exit 1
		else
		     	echo "started stream"
		fi
		sleep 10
	     	./scripts/8-wait_for_safestream.sh
	     	ret=$?
	     	if [ $ret -ne 0 ]; 
		then
			echo "failed"
			exit 1
	     	else
			echo "PASS"
	     	fi
	     	sleep 10
	     	echo $a
	     	a=`expr $a + 1`
	done
	echo "load test done"
fi
