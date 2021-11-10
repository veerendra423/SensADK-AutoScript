#!/bin/sh
#make sure you are running these script inside safectl and after running ./scripts/allgroups.sh
a=0

source test.env

while [ $a -lt 10 ]

do
   #./scripts/7-safestream_operator.sh
   #sleep 20
   #./scripts/7-safestream_operator.sh
   #ret=$?
   #if [ $ret -ne 0 ]; then
   #     echo "failed"
  #      exit 1
  # else
   #     echo "started stream"
   #fi

   #sleep 10
   ./scripts/7-safestream_operator.sh
   ret=$?
   if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
   else
        echo "started stream"
   fi
   sleep 20

   ./scripts/8-wait_for_safestream.sh
   ret=$?
   if [ $ret -ne 0 ]; then
        echo "failed"
        exit 1
   else
        echo "PASS"
   fi
   sleep 20
   echo $a
   a=`expr $a + 1`
done

