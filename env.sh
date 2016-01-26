#!/usr/bin/bash
#source env.sh please

# apt-get install git -y
# hostname spider0
# adduser cxy
# cd /home/cxy
# git clone https://github.com/aquairus/lemon_spiders.git
# source env.sh
echo "mail?"
read mail
export mailuser="$mail"

echo "pass?"
read pass
export passwd="$pass"

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
apt-get install redis-server python-pip -y
#if master

pip2.7 install redis progressive hiredis
pip2.7 install requests beautifulsoup4 threadpool pybloom  bitarray lxml

cat spider_list >>/etc/hosts
