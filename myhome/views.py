from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
import serial
from django.shortcuts import render, get_object_or_404
from myhome.models import Seneor
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
import json


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
         data_display = arduinoData.strip('\n').strip('\r')
         print(data_display)
         Tvalue = float(data_display[:5])
         Hvalue = float(data_display[6:11])
         Uvalue = int(data_display[12:])
         print(Tvalue)
         print(Hvalue)
         print(Uvalue)

         data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
         data.save()
         context = {'data': data}

     return render(request, 'myhome:connection', context)


class IndexView(generic.ListView):
    template_name = "showdata.html"
    context_object_name = "all_data"

    def get_queryset(self):
        return Seneor.objects.all().order_by('-time')[:1]




class HistoryView(generic.ListView):
    template_name = "history.html"

    def get_queryset(self):
        alldata = Seneor.objects.all().order_by('-time')[:100]
        data = []

        # for _ in alldata:
        #     json_data = {
        #         "id": _.id,
        #         "Tvalue":_.Tvalue
        #     }
        #
        #     data.insert(0,json_data)
        #
        # print(data)
        count = 1
        average_value = 0
        total_value = 0
        time_hour = 1
        for _ in alldata:
            if count % 10!=0:
                total_value = total_value + _.Tvalue
                count = count + 1

            else:
                count = 1
                average_value = total_value/10
                print(total_value)
                print("average:", average_value)
                json_data = {
                    "id": time_hour,
                    "Tvalue": average_value
                }
                print(average_value)
                data.insert(0, json_data)
                time_hour = time_hour + 1
                total_value = 0
        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        return alldata


