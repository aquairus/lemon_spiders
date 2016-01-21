#!/usr/bin/bash
chmod 700 ~/.ssh 
cp id_rsa.pub ~/.ssh/id_rsa.pub
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

apt-get install python-dev libxml2 libxml2-dev python-lxml -y #python-devel
pip install requests beautifulsoup4 threadpool pybloom  bitarray lxml

