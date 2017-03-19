from django.shortcuts import render
from django.http import HttpResponse
from sshtest import sshtest
from ftptest import ftptest
from httptest import httptest
from dnstest import dnstest
from sqltest import sqltest
from researchapp.forms import *
from researchapp.models import Service, LoginInfo
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
User.objects.all().delete() 
Group.objects.all().delete()
user = User.objects.create_user(username='whiteteam', password='whiteteamisawesome')
user.save()
whiteteam = Group()
whiteteam.name = "whiteteam"
whiteteam.save()
whiteteam = Group.objects.get(name='whiteteam') 
whiteteam.user_set.add(user)
blueteam = Group()
blueteam.name = "blueteam"
blueteam.save()
blueteam = Group.objects.get(name='blueteam')

def login(request):
	if request.method == "POST":
		loginData = LoginForm(request.POST)
		if loginData.is_valid():
			username = loginData.cleaned_data['username']
			password = loginData.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				request.session['username'] = username
				return render(request, 'loggedin.html', {"login_username" : username })
			else:
				return render(request, 'loginpage.html')
	elif request.method == "GET":
		return render(request, 'loginpage.html')
	else:
		loginData = LoginForm()
		
def formView(request):
	if request.session.has_key('username'):
		username = request.session['username']
		return render(request, 'loggedin.html', {"login_username" : username })
	else:
		return render(request, 'loginpage.html')
		
def settings(request):
	return render(request, 'settings.html', {"login_username" : request.session['username'] })
	
def logout(request):
	try:
		del request.session['username']
	except:
		pass
	return render(request, 'loginpage.html')
		
def addteam(request):
	if request.method == "POST":
		addteamData = LoginForm(request.POST)
		if addteamData.is_valid():
			username = addteamData.cleaned_data['username']
			password = addteamData.cleaned_data['password']
			adduser(username, password, blueteam)
			setDefaultCreds(username)
	return render(request, 'settings.html', {"login_username" : request.session['username'] })
	
def setDefaultCreds(teamnumber):
	ftp = Service()
	ftp.teamnumber = teamnumber
	ftp.servicename = "ftp"
	ftp.ip_address = '127.0.0.1'
	ftp.username = teamnumber
	ftp.password = teamnumber
	ftp.port = 21
	ftp.save()
	ssh = Service()
	ssh.teamnumber = teamnumber
	ssh.servicename = "ssh"
	ssh.ip_address = '127.0.0.1'
	ssh.username = teamnumber
	ssh.password = teamnumber
	ssh.port = 22
	ssh.save()
	dns = Service()
	dns.teamnumber = teamnumber
	dns.servicename = "dns"
	dns.ip_address = '127.0.0.1'
	dns.username = "NA"
	dns.password = "NA"
	dns.port = 53
	dns.save()
	http = Service()
	http.teamnumber = teamnumber
	http.servicename = "http"
	http.ip_address = '127.0.0.1'
	http.username = "NA"
	http.password = "NA"
	http.port = 80
	http.save()
	sql = Service()
	sql.teamnumber = teamnumber
	sql.servicename = "sql"
	sql.ip_address = '127.0.0.1'
	sql.username = teamnumber
	sql.password = teamnumber
	sql.port = 3306
	sql.save()
	
def changepassword(request):
	if request.method == "POST":
		loginData = LoginForm(request.POST)
		if loginData.is_valid():
			password = loginData.cleaned_data['password']
			user.set_password('password')
	return render(request, 'settings.html', {"login_username" : request.session['username'] })
			
def adduser(username, password, group):
	user = User.objects.create_user(username=username, password=password)
	user.save()
	group.user_set.add(user)
	
def teamhome(request):
	services = Service.objects.filter(teamnumber=request.session['username'])
	return render(request, 'teamhome.html', {"login_username" : request.session['username'], "service_list" : services})

def index(request):
	return HttpResponse("Hello, world. You're at the research app index.")

def ssh(request):
	ssh = Service.objects.filter(teamnumber=request.session['username'], servicename="ssh").values()
	service = ssh[0]
	runsshtest = sshtest(service['ip_address'], service['username'], service['password'], service['port'])
	value = runsshtest.sshtest()
	return value
		
def sshStatus(request):
	print "ssh status"
	sshObject = ssh(request)
	if sshObject is True:
		return HttpResponse("SSH is up.")
	else:
		return HttpResponse("SSH is not up.")
		
def ftp(request):
	ftp = Service.objects.filter(teamnumber=request.session['username'], servicename="ftp").values()
	service = ftp[0]
	runftptest = ftptest(service['ip_address'], service['username'], service['password'])
	value = runftptest.ftptest()
	return value
		
def ftpStatus(request):
	print "ftp status"
	ftpObject = ftp(request)
	if ftpObject is True:
		return HttpResponse("FTP is up.")
	else:
		return HttpResponse("FTP is not up.")
		
def ftpSave(request):
	if request.method == "POST":
		MyFtpData = ServiceForm(request.POST)
		if MyFtpData.is_valid():
			ip_address_ftp = MyFtpData.cleaned_data['ip_address']
			username_ftp = MyFtpData.cleaned_data['username']
			password_ftp = MyFtpData.cleaned_data['password']
			port_ftp = MyFtpData.cleaned_data['port']
			Service.objects.filter(teamnumber=request.session['username'], servicename="ftp").update(ip_address=ip_address_ftp)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ftp").update(username=username_ftp)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ftp").update(password=password_ftp)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ftp").update(port=port_ftp)
	else:
		MyFtpForm = ServiceForm()		
	return render(request, 'teamhome.html', {"login_username" : request.session['username'],"ip_address" : ip_address_ftp, "username" : username_ftp, "password" : password_ftp, "port" : port_ftp})
		
def http(request):
	http = Service.objects.filter(teamnumber=request.session['username'], servicename="http").values()
	service = http[0]
	runhttptest = httptest(service['ip_address'])
	value = runhttptest.httptest()
	return value
	
def httpStatus(request):
	httpObject = http(request)
	if httpObject is True:
		return HttpResponse("HTTP is up.")
	else:
		return HttpResponse("HTTP is not up.")
		
def httpSave(request):
	if request.method == "POST":
		print "got here"
		MyHttpData = ServiceFormNoLogin(request.POST)
		if MyHttpData.is_valid():
			print "valid"
			ip_address_http = MyHttpData.cleaned_data['ip_address']
			username_http = "NA"
			password_http = "NA"
			port_http = MyHttpData.cleaned_data['port']
			Service.objects.filter(teamnumber=request.session['username'], servicename="http").update(ip_address=ip_address_http)
			Service.objects.filter(teamnumber=request.session['username'], servicename="http").update(username=username_http)
			Service.objects.filter(teamnumber=request.session['username'], servicename="http").update(password=password_http)
			Service.objects.filter(teamnumber=request.session['username'], servicename="http").update(port=port_http)
	else:
		MyHttpForm = ServiceFormNoLogin()		
	return render(request, 'teamhome.html', {"login_username" : request.session['username'], "ip_address" : ip_address_http, "username" : username_http, "password" : password_http, "port" : port_http})
		
def dns(request):
	dns = Service.objects.filter(teamnumber=request.session['username'], servicename="dns").values()
	service = dns[0]
	print service['teamnumber'] + ".com"
	rundnstest = dnstest(service['ip_address'], service['teamnumber'] + ".com")
	value = rundnstest.dnstest()
	return value
	
def dnsStatus(request):
	dnsObject = dns(request)
	if dnsObject is True:
		return HttpResponse("DNS is up.")
	else:
		return HttpResponse("DNS is not up.")
		
def dnsSave(request):
	if request.method == "POST":
		MyDnsData = ServiceFormNoLogin(request.POST)
		if MyDnsData.is_valid():
			ip_address_dns = MyDnsData.cleaned_data['ip_address']
			username_dns = "NA"
			password_dns = "NA"
			port_dns = MyDnsData.cleaned_data['port']
			Service.objects.filter(teamnumber=request.session['username'], servicename="dns").update(ip_address=ip_address_dns)
			Service.objects.filter(teamnumber=request.session['username'], servicename="dns").update(username=username_dns)
			Service.objects.filter(teamnumber=request.session['username'], servicename="dns").update(password=password_dns)
			Service.objects.filter(teamnumber=request.session['username'], servicename="dns").update(port=port_dns)
	else:
		MyDnsForm = ServiceFormNoLogin()		
	return render(request, 'teamhome.html', {"login_username" : request.session['username'], "ip_address" : ip_address_dns, "username" : username_dns, "password" : password_dns, "port" : port_dns})
		
def sql(request):
	sql = Service.objects.filter(teamnumber=request.session['username'], servicename="sql").values()
	service = sql[0]
	runsqltest = sqltest(service['ip_address'], service['username'], service['password'])
	value = runsqltest.sqltest()
	return value
	
def sqlStatus(request):
	sqlObject = sql(request)
	if sqlObject is True:
		return HttpResponse("MySQL is up.")
	else:
		return HttpResponse("MySQL is not up.")
		
def sqlSave(request):
	if request.method == "POST":
		MySqlData = ServiceForm(request.POST)
		if MySqlData.is_valid():
			ip_address_sql = MySqlData.cleaned_data['ip_address']
			username_sql = MySqlData.cleaned_data['username']
			password_sql = MySqlData.cleaned_data['password']
			port_sql = MySqlData.cleaned_data['port']
			Service.objects.filter(teamnumber=request.session['username'], servicename="sql").update(ip_address=ip_address_sql)
			Service.objects.filter(teamnumber=request.session['username'], servicename="sql").update(username=username_sql)
			Service.objects.filter(teamnumber=request.session['username'], servicename="sql").update(password=password_sql)
			Service.objects.filter(teamnumber=request.session['username'], servicename="sql").update(port=port_sql)
	else:
		MySqlForm = ServiceForm()
		
	return render(request, 'teamhome.html', {"login_username" : request.session['username'], "ip_address" : ip_address_sql, "username" : username_sql, "password" : password_sql, "port" : port_sql})
		
def status(request):
	toReturn = "SSH Status: ", ssh(request)
	toReturn += "<br>FTP Status: ", ftp(request)
	toReturn += "<br>HTTP Status: ", http(request)
	toReturn += "<br>DNS Status: ", dns(request)
	toReturn += "<br>MySQL Status: ", sql(request)
	return HttpResponse(toReturn)
	
def sshSave(request):
	if request.method == "POST":
		MySshData = ServiceForm(request.POST)
		if MySshData.is_valid():
			ip_address_ssh = MySshData.cleaned_data['ip_address']
			username_ssh= MySshData.cleaned_data['username']
			password_ssh = MySshData.cleaned_data['password']
			port_ssh = MySshData.cleaned_data['port']
			Service.objects.filter(teamnumber=request.session['username'], servicename="ssh").update(ip_address=ip_address_ssh)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ssh").update(username=username_ssh)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ssh").update(password=password_ssh)
			Service.objects.filter(teamnumber=request.session['username'], servicename="ssh").update(port=port_ssh)
	else:
		MySshForm = ServiceForm()
		
	return render(request, 'teamhome.html', {"login_username" : request.session['username'], "ip_address" : ip_address_ssh, "username" : username_ssh, "password" : password_ssh, "port" : port_ssh})
	
def sshIn(request):
	return render(request, 'sshinput.html', {"login_username" : request.session['username']})
	
def ftpIn(request):
	return render(request, 'ftpinput.html', {"login_username" : request.session['username']})
	
def httpIn(request):
	return render(request, 'httpinput.html', {"login_username" : request.session['username']})
	
def dnsIn(request):
	return render(request, 'dnsinput.html', {"login_username" : request.session['username']})
	
def sqlIn(request):
	return render(request, 'sqlinput.html', {"login_username" : request.session['username']})
	
def databaseTest(request):
	ssh = Ssh.objects.get(port=22022)
	return render(request, 'sshoutput.html', {"ip_address" : ssh.ip_address, "username" : ssh.username, "password" : ssh.password, "port" : ssh.port})
	
