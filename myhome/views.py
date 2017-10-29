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

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from .forms import  RegisterForm, UserInfoForm


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
         data_display = arduinoData.replace(',', '').strip('\n').strip('\r')
         print(data_display)
         Tvalue = float(data_display[:5])
         Hvalue = float(data_display[5:10])
         Uvalue = int(data_display[10:])
         print(Tvalue)
         print(Hvalue)
         print(Uvalue)

         data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
         data.save()

         if (Uvalue <= 2):
             if(Hvalue <=40):
                 context = {'UVNote': 'UV value is low. You can go out and have fun!',
                            'HNote': 'Humidity value is too low for your skin',
                            'data': data}
             elif(Hvalue >40 and Hvalue<=60):
                 context = {'UVNote': 'UV value is low. You can go out and have fun!',
                            'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
                            'data': data}

         elif(Uvalue > 2 and Uvalue <= 5):
             context = {'UVNote': 'UV value is moderate. You can go out and fun! But you’d better to use sunscreen(SPF30) or sunglasses to protect your skin from aging causing by UV.',
                           'data': data}
         elif(Uvalue > 5 and Uvalue <= 7):
             context = {'UVNote': 'UV value is high. Please use appropriate protection like sunscreen (SPF 50++), sunglasses, sun-protective clothing or slap.',
                        'data': data}
         elif(Uvalue > 8 and Uvalue <= 10):
             context = {'UVNote': 'UV value is very high. You’d better stay indoors or use appropriate protection like sunscreen (SPF 50+++), sunglasses, sun-protective clothing or slap.',
                        'data': data}
         else:
            context = {'UVNote': 'UV value is extremely strong. You should better stay indoors. The sun ultraviolet (UV) radiation is the major cause of skin cancer and cause of skin aging.',
                        'data': data}

         break

     ser.close()

     return render(request, 'myhome.html', context)


def ArdunioReadLong(request):

     ser = serial.Serial("/dev/cu.usbmodem1411", baudrate=9600)

     count = 0

     while 1:
         arduinoData = ser.readline().decode('ascii')
         print(arduinoData)
         data_display = arduinoData.replace(',', '').strip('\n').strip('\r')
         print(data_display)
         Tvalue = float(data_display[:5])
         Hvalue = float(data_display[5:10])
         Uvalue = int(data_display[10:])
         print(Tvalue)
         print(Hvalue)
         print(Uvalue)

         data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
         data.save()

         count = count + 1

         if (count >= 2000):
            context = {'Loding': 'You have read 10 groups of value'}
            break
     ser.close()

     return render(request, 'myhome.html', context)

# class IndexView(generic.ListView):
#     template_name = "showdata.html"
#     context_object_name = "all_data"
#
#     def get_queryset(self):
#         return Seneor.objects.all().order_by('-time')[:1]
#
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         alldata = Seneor.objects.all().order_by('-time')[:1]
#         for _ in alldata:
#             if  _.Hvalue > 20:
#                context['Notification'] = "hot"
#                return context



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

      

class UV_valueView(generic.ListView):
    template_name = "UV.html"
    def get_queryset(self):
        alldata = Seneor.objects.all().order_by('-time')[:100]
        return alldata




def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            my_login(request, user)
            return render(request, "showdata.html")
        else:
            context = {'login_err': 'Username or Password is wrong!'}
            return render(request, "login.html", context)
    elif request.method == "GET":
        return render(request, "login.html",{})


def my_login(request, user):
    login(request, user)
    request.session['user_id'] = user.id


def user_logout(request):
    my_logout(request)
    return HttpResponseRedirect("/myhome")


def my_logout(request):
    logout(request)
    request.session['user_id'] = ''


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            my_register(request, username, password)
            return HttpResponseRedirect("/myhome")
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form': form})


def my_register(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        my_login(request, user)

def Userinfo(request):
    return  render(request, 'user_profile.html',{})

def editprofile(request):
    user_info_form = UserInfoForm(request.POST, instance=request.user)
    if user_info_form.is_valid():
        user_info_form.save()
        return HttpResponseRedirect("/myhome/info")
    else:
        user_info_form = UserInfoForm()
    return render(request, 'edit_profile.html', context={'user_info_form': user_info_form})




