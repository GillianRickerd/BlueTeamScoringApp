import MySQLdb

class sqltest:
	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password

	def sqltest(self):
		dbstatus = False
		try:
			db = MySQLdb.connect(self.host,self.user,self.password)
			dbstatus = True
			db.close()
		except:
			dbstatus = False
		return dbstatus
