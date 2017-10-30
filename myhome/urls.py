from django.conf.urls import url
from . import views

app_name = 'myhome'

urlpatterns = [
    url(r'^index', views.IndexView.as_view(), name='index'),
    url(r'^$', views.MyHomeListView.as_view(), name='myhome'),
    url(r'^testCon$', views.ArdunioConnection, name='connection'),
    url(r'^ReadLong$', views.ArdunioReadLong, name='readlong'),
    url(r'^historyofTvalue', views.History_TvalueView.as_view(), name='historyofTvalue'),
    url(r'^historyofUvalue', views.History_UvalueView.as_view(), name='historyofUvalue'),
    url(r'^historyofHvalue', views.History_HvalueView.as_view(), name='historyofHvalue'),
    url(r'^UV', views.UV_valueView.as_view(), name='uvValue'),

    url(r'^week_Hvalue', views.week_HvalueView.as_view(), name='week_Hvalue'),
    url(r'^week_Tvalue', views.week_TvalueView.as_view(), name='week_Tvalue'),
    url(r'^week_Uvalue', views.week_UvalueView.as_view(), name='week_Uvalue'),

    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^register/', views.register, name='register'),
    url(r'^info/', views.Userinfo, name='info'),
    url(r'^edit_profile/', views.editprofile, name='edit_profile'),
]