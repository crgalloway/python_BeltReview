from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^books$',views.books),
	url(r'^books/add$',views.add),
	url(r'^logout$',views.logout),
	url(r'^process$',views.processAdd),
	url(r'^users/(?P<number>\d+)$',views.users),
	url(r'^books/(?P<number>\d+)$',views.bookInfo),
	url(r'^processReview$',views.processReview),
	url(r'^destroy/(?P<number>\d+)$',views.destroy),
]