"""SkinHealth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib import admin
from myhome import views
from Data.views import DataHistoryView
from Data.views import APIDataHistoryView

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', views.MyHomeListView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('authentication.urls', namespace='authentication')),
    url(r'^myhome/', include('myhome.urls', namespace='myhome')),
    url(r'^registration/', include('registration.urls', namespace='registration')),
    url(r'^Data/history/$', DataHistoryView.as_view(), name='raw-data-data-trend'),
    # Raw Data API
    url(r'^api/Data/history/$', APIDataHistoryView.as_view(), name='api-data-history'),
]
