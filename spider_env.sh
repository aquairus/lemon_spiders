#!/usr/bin/bash
echo "mail?"
read mail
export mail

echo "pass?"
read pass
export pass

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
#apt-get install redis-server -y	
#if master

pip install redis progressive hiredis 
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml

