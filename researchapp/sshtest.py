import paramiko

class sshtest:
	def __init__(self, ip, user, password, port):
		self.ip = ip
		self.user = user
		self.password = password
		self.port = port
		
		
	def sshtest(self):
		print 'ip', self.ip
		print 'user', self.user
		print 'pass', self.password
		print 'port', self.port
		sshstatus = False
		try: 
			print "start try"
			client = paramiko.SSHClient()
			print "step 2"
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			print "step 3"
			client.connect(self.ip, username=self.user, password=self.password, port=self.port)
			print "connect"

			# stdin, stdout, stderr = client.exec_command("which sshd")
			# if stdout is not None:
			sshstatus = True
			client.close()
		except: 
			print "except"
			sshstatus = False
		return sshstatus
