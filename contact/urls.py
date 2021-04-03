from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.contact, name='contact'),
    url(r'^done/$', views.done, name='done'),
]
