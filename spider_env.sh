#!/usr/bin/bash

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
#apt-get install redis-server -y	
#if master

pip install redis progressive hiredis 
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml

