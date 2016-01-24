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


class mailbox():
    """docstring for mailbox"""
    def __init__(self,user,passwd):
        self.to_addr ="443586791@qq.com"
        self.user=user
        self.password=passwd
        smtp_server = "smtp.163.com"
        self.server = smtplib.SMTP(smtp_server, 25)

    def login(self):
        return self.server.login(self.user, self.password )

    def send_msg(self,sender,content):

     	hostname=socket.gethostname()
    	msg = MIMEText(hostname+"("+sender+"):\n"+content, 'plain', 'utf-8')
    	msg['From'] = _format_addr(sender+u'<%s>' % self.user)
    	msg['To'] = _format_addr(u'spider manager <%s>' % self.to_addr)
    	msg['Subject'] = Header(u'spider info update', 'utf-8').encode()
    	print self.server.sendmail(self.user, [self.to_addr], msg.as_string())
    	self.server.quit()
