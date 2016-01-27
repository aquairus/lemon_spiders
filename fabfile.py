
from fabric.api import cd,run,env,hosts,roles,execute,settings,local

import os


if os.environ['pass']:
	env.password=os.environ['pass']
else:
	print "enter your password,honey?"
	env.password=raw_input()



env.roledefs = {
'master': ['root@spider01'],

'slaver': ['root@spider02','root@spider03',\
'root@spider04','root@spider05','root@spider06'],

'all':['root@spider01','root@spider02','root@spider03',\
'root@spider04','root@spider05','root@spider06']

}


@roles('master')
def get_master():
	run("hostname")


@roles('slaver')
def get_slaver():
	run("hostname")

@roles('all')
def ls():
	with cd('/home/cxy/lemon_spiders'):
 		run("ls")




@roles('all')
def update():
	with cd('/home/cxy/lemon_spiders'):
 		run ("git reset --hard")
 		run("git pull")

def get_all():
	execute(get_master)
	execute(get_slaver)

def new_node(host):
	env.user="root"
	with settings(warn_only=True):
		run('apt-get install git -y')
		run('hostname '+host)
		run('adduser cxy')
		run('git clone https://github.com/aquairus/lemon_spiders.git \
			/home/cxy/lemon_spiders')
		run('source /home/cxy/lemon_spiders/conf/env.sh')
#fab new_node:spider -H spider

def save():
	local("git add -A")
	local("git commit -m 'save' ")
	local("git push")


