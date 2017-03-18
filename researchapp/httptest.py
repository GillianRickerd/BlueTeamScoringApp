import requests


class httptest:
	def __init__(self, ip):
		self.ip = ip	
		
	def httptest(self):
		webstatus = False

		request = requests.get("http://" + self.ip)
		if request.status_code is 200:
			webstatus = True
		return webstatus
