from django.conf.urls import url, include

urlpatterns = [
	url(r'^', include('apps.beltReview_app.urls')),
]