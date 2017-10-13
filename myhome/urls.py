from django.conf.urls import url
from . import views

app_name = 'myhome'

urlpatterns = [
    url(r'^$', views.MyHomeListView.as_view(), name='myhome'),
    url(r'^testCon$', views.ArdunioConnection, name='connection'),
]