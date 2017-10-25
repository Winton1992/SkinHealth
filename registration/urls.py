from django.conf.urls import url
from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    # url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/edit/$', views.edit_user, name='account_update'),
]
