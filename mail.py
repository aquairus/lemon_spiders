#-*- coding:UTF-8 -*- 

import smtplib
import os
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from time import sleep
import socket  

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_msg(sender,content):
	from_addr = os.environ['mail']
	password = os.environ['pass']
	smtp_server = "smtp.163.com"
	to_addr ="443586791@qq.com"

	msg = MIMEText(sender+":\n"+content, 'plain', 'utf-8')
	msg['From'] = _format_addr(sender+u'<%s>' % from_addr)
	msg['To'] = _format_addr(u'spider manager <%s>' % to_addr)
	msg['Subject'] = Header(u'spider info update', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25) 
	#server.set_debuglevel(3)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
