email-client
=======

This is simple smtp/pop3 client writen as university project .The project also include server configuration that will be added later

Installation 
-----------

Installl on debian / ubuntu : 

	apt-get update 
	apt-get install python3 python3-pyqt4 git
	git clone git@github.com:ghobadimhd/email-client.git
	
To run client : 
	
	cd email-client 
	./email-clinet 

Setting 
-------

For now client use simple setting file '.setting' .The format is like Windows ini files like below : 

	[DEFAULT]
	smtp_server = 127.0.0.1 
	smtp_user = username
	smtp_pass = 123 
	pop3_server = 127.0.0.1 
	pop3_user = username 
	pop3_pass = 123
