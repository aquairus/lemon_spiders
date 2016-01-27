
from fabric.api import cd,run,env,hosts,roles,execute,settings,local
import pysftp
import os

slaver_list=['spider02','spider03',\
'spider04','spider05','spider06']


try:
	env.password=os.environ['spider_pass']
	ftp_passwd=os.environ['ftp_pass']
except BaseException, e:
	print "enter spider_pass,honey"
	env.password=raw_input()
	print "enter ftp_password,honey"
	ftp_passwd=raw_input()

env.user="root"

env.roledefs = {
'master': ['spider01'],

'slaver': slaver_list,

'all':['spider01']+slaver_list

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

def download(name,r_dir="/home/cxy"):
	
	usr="cxy"

	l_dir='/Users/apple/Desktop/'+name

	with settings(warn_only=True):
		local("mkdir "+l_dir)

	for slaver in slaver_list:
		with pysftp.Connection(slaver,\
		 username=usr, password=ftp_passwd) as sftp:
			try:
				sftp.get_d(r_dir,l_dir)
			except BaseException, e:
				pass
