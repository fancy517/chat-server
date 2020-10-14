from django.conf.urls import include, url
from django.contrib import admin
from chat import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api/getMessages', views.getMessages, name='getMessages'),
]
