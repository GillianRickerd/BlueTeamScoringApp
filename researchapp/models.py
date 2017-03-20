from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Service(models.Model):
	teamnumber = models.CharField(max_length=15)
	servicename = models.CharField(max_length=15)
	ip_address = models.CharField(max_length=15)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	port = models.IntegerField()
	status = models.BooleanField()
	
	class Meta:
		db_table = "service"

class LoginInfo(models.Model):
	teamnumber = models.IntegerField()
	roundnumber = models.IntegerField()
	servicename = models.CharField(max_length=10)
	status = models.BooleanField() 
	
	class Meta:
		db_table = "logininfo"
