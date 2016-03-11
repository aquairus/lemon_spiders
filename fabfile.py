
from fabric.api import cd,run,env,hosts,roles,execute,settings,local
import os

slaver_list=['spider02','spider03',\
'spider05','spider06']
#04

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






@roles('all')
def do():
	run("git config --global user.email 18650013469@163.com ")
	run("git config --global user.name cxy")


@roles('all')
def ls():
	with cd('/home/cxy'):
 		run ("ls -l")
 		run ("du -sh *")
 		run ("date")



@roles('all')
def update():
	with cd('/home/cxy/lemon_spiders'):
 		run ("git reset --hard HEAD^^^")
 		run("git pull")

# @roles('all')
# def install ():
# 	run("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7")
# 	run("echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list")
# 	run("sudo apt-get update && sudo apt-get install scrapy -y")
# 	run("pip install service-identity")
# 	run("easy_install pyasn1-modules")


def new_node(host):
	with settings(warn_only=True):
		run('apt-get install git -y')
		run('hostname '+host)
		run('adduser cxy')
		run('git clone https://github.com/aquairus/lemon_spiders.git \
			/home/cxy/lemon_spiders')
		run('source /home/cxy/lemon_spiders/conf/env.sh')

def save():
	local("git add -A")
	with settings(warn_only=True):
		local("git commit -m 'save' ")
		local("git push")




@roles('slaver')
def work():
	with cd('/home/cxy/lemon_spiders'):
 		run("screen -S work")

@roles('slaver')
def check():
	with cd('/home/cxy/lemon_spiders'):
 		run("screen -r work")

@roles('slaver')
def clean():
	with cd('/home/cxy'):
 		run("rm yahoo*")

@roles('master')
def direct():
	with cd('/home/cxy/lemon_spiders'):
 		run("screen -S direct")

def start():
	execute(save)
	execute(update)
	execute(direct)
	execute(work)
