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
from django.shortcuts import render_to_response
from django.template import RequestContext


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


# class IndexView(generic.ListView):
#     template_name = "showdata.html"
#     context_object_name = "all_data"
#
#     def get_queryset(self):
#         return Seneor.objects.all().order_by('-time')[:1]
class IndexView(generic.ListView):
    template_name = "showdata.html"
    context_object_name = "all_data"

    def get_queryset(self):
        return Seneor.objects.all().order_by('-time')[:1]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        alldata = Seneor.objects.all().order_by('-time')[:1]
        for _ in alldata:
            if  _.Hvalue > 20:
               context['Notification'] = "hot"
               return context


class History_TvalueView(generic.ListView):
    template_name = "historyofTvalue.html"
    context_object_name = "Notification"

    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
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
        total_val = 0
        time_hour = 1
        for _ in daydata:
            total_val = total_val + _.Tvalue
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

        if total_val / 10 > 20:
             Notification = "Warning: The temperature is too hign."
             return Notification


class History_UvalueView(generic.ListView):
    template_name = "historyofUvalue.html"
    context_object_name = "Notification"
    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        data = []
        total_val = 0
        count = 1
        average_value = 0
        total_value = 0
        time_hour = 1
        for _ in daydata:
            total_val = total_val + _.Hvalue
            if count % 10!=0:
                total_value = total_value + _.Uvalue
                count = count + 1

            else:
                count = 1
                average_value = total_value/10
                print(total_value)
                print("average:", average_value)
                json_data = {
                    "id": time_hour,
                    "Uvalue": average_value
                }
                print(average_value)
                data.insert(0, json_data)
                time_hour = time_hour + 1
                total_value = 0
        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 10 > 50:
             Notification = "Warning: You were exposed under high UV value."
             return Notification


class History_HvalueView(generic.ListView):
    template_name = "historyofHvalue.html"
    context_object_name = "Notification"

    def get_queryset(request):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        weekdata = Seneor.objects.all().order_by('-time')[:240]
        data = []
        count = 1
        average_value = 0
        total_value = 0
        hour = 1
        total_val = 0
        for _ in daydata:
            total_val = total_val + _.Hvalue
            if count % 10 != 0:
                total_value = total_value + _.Hvalue
                count = count + 1

            else:
                count = 1
                average_value = total_value / 10
                print(total_value)
                print("average:", average_value)
                json_data = {
                    "id": hour,
                    "Hvalue": average_value
                }
                print(average_value)
                data.insert(0, json_data)
                hour = hour + 1
                total_value = 0


        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)


        if total_val / 10 > 50:
             Notification = "Warning: The Humid value in your environment is too high."
             return Notification

        #week data
        # for _ in weekdata:
        #     total_val = total_val + _.Hvalue
        #     if count % 10 != 0:
        #         total_value = total_value + _.Hvalue
        #         count = count + 1
        #
        #     else:
        #         count = 1
        #         average_value = total_value / 10
        #         print(total_value)
        #         print("average:", average_value)
        #         json_data = {
        #             "id": hour,
        #             "Hvalue": average_value
        #         }
        #         print(average_value)
        #         data.insert(0, json_data)
        #         hour = hour + 1
        #         total_value = 0
        #
        # with open('static/json/week_data.json', 'w') as outfile:
        #     json.dump(data, outfile)

class UV_valueView(generic.ListView):
    template_name = "UV.html"
    def get_queryset(self):
        alldata = Seneor.objects.all().order_by('-time')[:100]
        return alldata





