#!/usr/bin/expect -f
#make sure you need to copy pem files within 30seconds after running these script from other terminal two commands below. you need to run after getting root@aks-ssh:/#, where you ran laslog.sh script. you will get result on sensccf2 machine in these directory /home/ccf/laslogs/ 
#kubectl cp utils/cm-data/nodes-ssh/id_rsa $(kubectl get pod -l run=aks-ssh -o jsonpath='{.items[0].metadata.name}'):/id_rsa
#kubectl cp /data/sham/veerendra/ccf.pem  $(kubectl get pod -l run=aks-ssh -o jsonpath='{.items[0].metadata.name}'):/ccf.pem


#kubectl get nodes -o wide
spawn kubectl run -it --rm aks-ssh --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11
expect "root@aks-ssh:/# "
sleep 30
send "ls\r"
expect "id_rsa "
send "ls\r"
expect "ccf.pem"
send "scp -i id_rsa azureuser@10.240.0.5:/home/azureuser/laslogs/* .\r"
expect "Are you sure you want to continue connecting (yes/no)? "
send "yes\r"
expect "root@aks-ssh:/# "
send "scp -i ccf.pem strace* ccf@sensccf2.eastus.cloudapp.azure.com:/home/ccf/laslogs/\r"
expect "Are you sure you want to continue connecting (yes/no)? "
send "yes\r"
expect "root@aks-ssh:/# "
#send "ssh -i id_rsa azureuser@10.240.0.5\r"
#expect "Are you sure you want to continue connecting (yes/no)? "
#send "yes\r"
#expect "$ "
#send "ls\r"
#expect "laslogs "
#send "exit\r"
#expect "root@aks-ssh:/# "
send "exit\r"
