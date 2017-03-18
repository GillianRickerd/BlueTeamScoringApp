from ftplib import FTP

class ftptest:
	def __init__(self, ip, user, password):
		self.ip = ip
		self.user = user
		self.password = password

	def ftptest(self):
		ftpstatus = False
		try:
			ftp = FTP(self.ip)
			ftp.login(user=self.user, passwd=self.password)

			ftpstatus = True

			ftp.quit()
		except:
			ftpstatus = False

		return ftpstatus
