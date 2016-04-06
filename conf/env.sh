#!/usr/bin/bash
#source env.sh please

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
apt-get install redis-server python-pip -y
apt-get install zlib1g-dev gcc make git autoconf autogen automake pkg-config -y

pip install redis progressive hiredis scrapy_redis pymongo supervisor
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml


mkdir  ~/.ssh
touch  ~/.ssh/authorized_keys
cat /home/cxy/lemon_spiders/id_dsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
