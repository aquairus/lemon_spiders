#!/usr/bin/bash
#source env.sh please



apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
apt-get install redis-server python-pip -y

pip install redis progressive hiredis
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml

cat spider_list >>/etc/hosts
