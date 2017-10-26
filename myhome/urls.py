from django.conf.urls import url
from . import views

app_name = 'myhome'

urlpatterns = [
    url(r'^$', views.MyHomeListView.as_view(), name='myhome'),
    url(r'^testCon$', views.ArdunioConnection, name='connection'),
    url(r'^data$', views.IndexView.as_view(), name='data'),
    url(r'^historyofTvalue', views.History_TvalueView.as_view(), name='historyofTvalue'),
    url(r'^historyofUvalue', views.History_UvalueView.as_view(), name='historyofUvalue'),
    url(r'^historyofHvalue', views.History_HvalueView.as_view(), name='historyofHvalue'),
]