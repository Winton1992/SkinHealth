from django.conf.urls import url
from . import views

app_name = 'myhome'

urlpatterns = [
    url(r'^$', views.MyHomeListView.as_view(), name='myhome'),
    url(r'^testCon$', views.ArdunioConnection, name='connection'),
    url(r'^ReadLong$', views.ArdunioReadLong, name='readlong'),
    url(r'^historyofTvalue', views.History_TvalueView.as_view(), name='historyofTvalue'),
    url(r'^historyofUvalue', views.History_UvalueView.as_view(), name='historyofUvalue'),
    url(r'^historyofHvalue', views.History_HvalueView.as_view(), name='historyofHvalue'),
    url(r'^UV', views.UV_valueView.as_view(), name='uvValue'),
    # url(r'^currentHvalue', views.Current_Humidity_valueVieww.as_view(), name='currentHvalue'),
    # url(r'^currentTvalue', views.Current_Temperature_valueView.as_view(), name='currentTvalue'),
    # url(r'^currentUvalue', views.Current_UV_valueView.as_view(), name='currentUvalue'),

    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^register/', views.register, name='register'),
    url(r'^info/', views.Userinfo, name='info'),
    url(r'^edit_profile/', views.editprofile, name='edit_profile'),
]