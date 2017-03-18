from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^ssh$', views.sshStatus, name='ssh'),
	url(r'^ftp$', views.ftpStatus, name='ftp'),
	url(r'^http$', views.httpStatus, name='http'),
	url(r'^dns$', views.dnsStatus, name='dns'),
	url(r'^mysql$', views.sqlStatus, name='sql'),
	url(r'^status$', views.status, name='status'),
	url(r'^sshIn$', views.sshIn, name='sshIn'),
	url(r'^sshSave$', views.sshSave, name='sshSave'),
	url(r'^ftpIn$', views.ftpIn, name='ftpIn'),
	url(r'^ftpSave$', views.ftpSave, name='ftpSave'),
	url(r'^databaseTest$', views.databaseTest, name='databaseTest'),
	url(r'^login$', views.login, name='login'),
	url(r'^connection$', views.formView, name = 'loginform'),
	url(r'^settings$', views.settings, name = 'settingsform'),
	url(r'^addteam$', views.addteam, name = 'addteam'),
	url(r'^changepassword$', views.changepassword, name = 'changepassword'),
	url(r'^logout$', views.logout, name = 'logout'),
	url(r'^teamhome$', views.teamhome, name = 'teamhome'),
]
