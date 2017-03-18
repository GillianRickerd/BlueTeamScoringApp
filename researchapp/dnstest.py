import dns.resolver

class dnstest:
	def __init__(self, ip, domainName):
		self.ip = ip
		self.domainName = domainName

	def dnstest(self):
		dnsstatus = False
		try:
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [self.ip]
			answer = my_resolver.query(self.domainName)
			#print answer[0]
			dnsstatus = True
		except:
			dnsstatus = False
		return dnsstatus
