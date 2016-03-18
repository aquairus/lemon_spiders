#!/usr/bin/bash
#source env.sh please

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
apt-get install redis-server python-pip -y

pip install redis progressive hiredis
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml

cat spider_list >>/etc/hosts
mkdir  ~/.ssh
touch  ~/.ssh/authorized_keys
cat /home/cxy/lemon_spiders/id_dsa.pub >> ~/.ssh/authorized_keys
 chmod 600 ~/.ssh/authorized_keys
