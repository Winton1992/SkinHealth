from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
import serial
from django.shortcuts import render, get_object_or_404


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
    context = {'arduinoData': arduinoData}
    return render(request, 'myhome:connection', context)
