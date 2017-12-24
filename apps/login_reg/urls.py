from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.index),
	url(r'^registration$', views.registration),
	url(r'^friends$', views.friends),
	url(r'^add/(P?\d+)$', views.add),
	url(r'^profile/(P?\d+)$', views.profile),
	url(r'^remove/(P?\d+)$', views.remove)
]