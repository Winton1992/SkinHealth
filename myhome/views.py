from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
import serial
from django.shortcuts import render, get_object_or_404
from myhome.models import UV
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic


# Create your views here.
class MyHomeListView(LoginRequiredMixin, ListView):
    template_name = 'myhome.html'
    context_object_name = 'notifications'
    login_url = '/auth/login/'

    def get_queryset(self):
        result = Notification.objects.values()
        return result

def ArdunioConnection(request):

     ser = serial.Serial("/dev/cu.usbmodem1411", baudrate=9600)

     while 1:
         arduinoData = ser.readline().decode('ascii')
         print(arduinoData)
         data_display = arduinoData.split(',')
         Tvalue = data_display[0]
         Hvalue = data_display[1]
         Uvalue = data_display[2]
         println(Tvalue)

         # p = UV.objects.create(value=arduinoData)
         # p.save()


     context = {'arduinoData': arduinoData}
     return render(request, 'myhome:connection', context)


class IndexView(generic.ListView):
    template_name = "showdata.html"
    context_object_name = "all_data"

    def get_queryset(self):
        return UV.objects.all().order_by("-time")[:1]


class HistoryView(generic.ListView):
    template_name = "history.html"
    context_object_name = "all_data"

    def get_queryset(self):
        return UV.objects.all().order_by("-time")[:1]
        


