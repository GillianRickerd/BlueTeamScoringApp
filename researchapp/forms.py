from django import forms


class ServiceForm(forms.Form):
	ip_address = forms.CharField(max_length=15)
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)
	port = forms.IntegerField()
	
class LoginForm(forms.Form):
	username = forms.CharField(required=True, max_length=15)
	password = forms.CharField(required=True, max_length=50)

