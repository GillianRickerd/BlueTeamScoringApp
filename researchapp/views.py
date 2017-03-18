from django.shortcuts import render
from django.http import HttpResponse
from sshtest import sshtest
from ftptest import ftptest
from httptest import httptest
from dnstest import dnstest
from sqltest import sqltest
from researchapp.forms import ServiceForm, LoginForm
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
				return render(request, 'loggedin.html', {"username" : username })
			else:
				return render(request, 'loginpage.html')
	elif request.method == "GET":
		return render(request, 'loginpage.html')
	else:
		loginData = LoginForm()
		
def formView(request):
	if request.session.has_key('username'):
		username = request.session['username']
		return render(request, 'loggedin.html', {"username" : username })
	else:
		return render(request, 'loginpage.html')
		
def settings(request):
	return render(request, 'settings.html', {"username" : request.session['username'] })
	
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
	return render(request, 'settings.html', {"username" : request.session['username'] })
	
def changepassword(request):
	if request.method == "POST":
		loginData = LoginForm(request.POST)
		if loginData.is_valid():
			password = loginData.cleaned_data['password']
			user.set_password('password')
	return render(request, 'settings.html', {"username" : request.session['username'] })
			
def adduser(username, password, group):
	user = User.objects.create_user(username=username, password=password)
	user.save()
	group.user_set.add(user)
	
def teamhome(request):
	#ssh = Service.objects.filter(teamnumber=request.session['username'], servicename="ssh")
	#print ssh.values()
	#ftp = Service.objects.filter(teamnumber=request.session['username'], servicename="ftp")
	services = Service.objects.filter(teamnumber=request.session['username'])
	#print ftp.values()
	return render(request, 'teamhome.html', {"username" : request.session['username'], "service_list" : services})
	#return render(request, 'teamhome.html', {"username" : ssh[0].username, "ip_address" : ssh[0].ip_address, "port" : ssh[0].port, "password" : ssh[0].password, 
	#"username_ftp" : ftp[0].username, "ip_address_ftp" : ftp[0].ip_address, "port_ftp" : ftp[0].port, "password_ftp" : ftp[0].password})

def index(request):
	return HttpResponse("Hello, world. You're at the research app index.")

def ssh(request):
	print "ssh request"
	runsshtest = sshtest('127.0.0.1', 'gillian', 'gillylemke15', 22)
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
	print "ftp request"
	runftptest = ftptest('127.0.0.1', 'gillian', 'gillylemke15')
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
			ftp = Service()
			ftp.teamnumber = request.session['username']
			ftp.servicename = "ftp"
			ftp.ip_address = ip_address_ftp
			ftp.username = username_ftp
			ftp.password = password_ftp
			ftp.port = port_ftp
			ftp.save()
	else:
		MyFtpForm = ServiceForm()
	#teamhome(request)
		
	return render(request, 'teamhome.html', {"ip_address" : ip_address_ftp, "username" : username_ftp, "password" : password_ftp, "port" : port_ftp})
		
def http(request):
	runhttptest = httptest('127.0.0.1')
	value = runhttptest.httptest()
	return value
	
def httpStatus(request):
	httpObject = http(request)
	if httpObject is True:
		return HttpResponse("HTTP is up.")
	else:
		return HttpResponse("HTTP is not up.")
		
def dns(request):
	rundnstest = dnstest('8.8.8.8', 'jacobrickerd.com')
	value = rundnstest.dnstest()
	return value
	
def dnsStatus(request):
	dnsObject = dns(request)
	if dnsObject is True:
		return HttpResponse("DNS is up.")
	else:
		return HttpResponse("DNS is not up.")
		
def sql(request):
	runsqltest = sqltest('localhost', 'root', 'gillylemke15')
	value = runsqltest.sqltest()
	return value
	
def sqlStatus(request):
	sqlObject = sql(request)
	if sqlObject is True:
		return HttpResponse("MySQL is up.")
	else:
		return HttpResponse("MySQL is not up.")
		
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
			ip_address = MySshData.cleaned_data['ip_address']
			username = MySshData.cleaned_data['username']
			password = MySshData.cleaned_data['password']
			port = MySshData.cleaned_data['port']
			ssh = Service()
			ssh.teamnumber = request.session['username']
			ssh.servicename = "ssh"
			ssh.ip_address = ip_address
			ssh.username = username
			ssh.password = password
			ssh.port = port
			ssh.save()
	else:
		MySshForm = ServiceForm()
		
	return render(request, 'sshoutput.html', {"ip_address" : ip_address, "username" : username, "password" : password, "port" : port})
	
def sshIn(request):
	return render(request, 'sshinput.html')
	
def ftpIn(request):
	return render(request, 'ftpinput.html')
	
def databaseTest(request):
	ssh = Ssh.objects.get(port=22022)
	return render(request, 'sshoutput.html', {"ip_address" : ssh.ip_address, "username" : ssh.username, "password" : ssh.password, "port" : ssh.port})
	
