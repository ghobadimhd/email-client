server configuration
===========

##### Postfix :
	
	aptitude install postfix bind9 opendkim libsasl2 libsasl2-module sasl2-bin courier-pop

/etc/postfix/main.cf 

	mydomain = com
	myhostname = example
	mydestination = $myhostname localhost example.com 
	relay_domains = $mydestination
	mynetworks_style = host

	inet_interfaces = all

	milter_protocol = 2
	milter_default_action = accept
	smtpd_milters = inet:localhost:12301
	non_smtpd_milters = inet:localhost:12301
	
	smtpd_sasl_auth_enable = yes
	smtpd_sasl_security_options = noanonymous
	
	home_mailbox = Maildir/


##### sasl auxprobe
	pwcheck_method = auxprobe 
	auxprobe_plugin = sasldb
	mech_list = PLAIN LOGIN 
	log_level = 7


##### opendkim 

	mkdir -p /etc/opendkim/example.com
	cd  /etc/opendkim/example.com
	opendkim-genkey -s mail -d example.com

/etc/opendkim.conf : 

	syslog          yes
	syslogsuccess	yes
	Umask           002
	oversignheaders from
	canonicalization        relaxed/simple
	Mode                    sv
	domain          example.com
	selector        mail
	keyfile         /etc/opendkim/example.com/mail.private
	UserId          opendkim:opendkim
	Socket          inet:12301@localhost
	pidFile         /var/run/opendkim/opendkim.pid



##### courier-pop3 :

	PIDFILE=/var/run/courier/pop3d.pid
	MAXDAEMONS=40
	MAXPERIP=4
	POP3AUTH=
	POP3AUTH_ORIG=PLAIN LOGIN CRAM-MD5 CRAM-SHA1 CRAM-SHA256
	POP3AUTH_TLS=
	POP3AUTH_TLS_ORIG=LOGIN PLAIN
	POP3_PROXY=0
	PORT=110
	ADDRESS=0
	TCPDOPTS=-nodnslookup -noidentlookup
	LOGGEROPTS=-name=pop3d
	POP3DSTART=YES
	MAILDIRPATH=Maildir

/etc/courier/pop3d

	PIDFILE=/var/run/courier/pop3d.pid
	MAXDAEMONS=40
	MAXPERIP=4
	POP3AUTH="PLAIN LOGIN"
	POP3AUTH_ORIG="PLAIN LOGIN CRAM-MD5 CRAM-SHA1 CRAM-SHA256"
	POP3AUTH_TLS=""
	POP3AUTH_TLS_ORIG="LOGIN PLAIN"
	POP3_PROXY=0
	PORT=110
	ADDRESS=0
	TCPDOPTS="-nodnslookup -noidentlookup"
	LOGGEROPTS="-name=pop3d"
	POP3DSTART=YES
	MAILDIRPATH=Maildir


DNS server config 
------------------

named.conf.options 

	options {
		directory "/var/cache/bind";


		dnssec-validation auto;

		auth-nxdomain no;    # conform to RFC1035
		listen-on-v6 { any; };

		version "nothing" ; 
		allow-query { any; } ;
		allow-recursion {127.0.0.1 ;} ; 
		recursion yes ; 
	};

	logging {
		channel security_log {
		file "/var/log/named/named.log"  
		versions 1 ;
		} ; 
		category security { security_log ; } ; 
	} ; 

named.conf.local : 

	zone "example.com" IN {
		type master ; 
		file "master.example.com"  ; 
	}; 

/var/cache/bind/master.example.com : 

	$TTL 6h
	$ORIGIN example.com. 
	@	IN 	SOA	ns1.example.com.	admin@example.com. (
						2016091300 ;sn 
						6h	;try 
						1h	;retry 
						1w	;expire
						1m	;nx cache
						)
	@ 	IN	NS 	ns1.example.com.
	ns1	IN	A	10.0.0.1
	@	IN	A	10.0.0.1
	@ 	IN 	MX	10 	example.com.	
	@	IN	TXT	"v=spf1 +a +mx ~all"
	mail._domainkey IN      TXT     ( "v=DKIM1; k=rsa; "
          "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCe7R9tItEcPM6vmmUSU12BPCmC2uiDyYk+9Mcw66aFGiHHdBMLsFgOxwgb1yKP+Lnk8BJNsrVvU/LgN2gPiF9l2X4dtBW1zAdRUC2Mby4IqxPjaUsmQ4S0eAmgxWo8JopQv4C6csYS+CxcjRV3diWtS8mOHH0S2VfTv/ctP3TuEQIDAQRB" )  ; ----- DKIM key mail for example.com



