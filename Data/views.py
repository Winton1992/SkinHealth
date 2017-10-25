from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import csv
from csv2json import convert, load_csv, save_json

# url 'Data/history/'
class DataHistoryView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "title": 'raw-data-data-trend',
        }
        return render(request, "myhome/templates/history.html", context)


class APIDataHistoryView(APIView):
    def get(self, request, format=None, **kwargs):

        # with open('static/csv/data.csv') as r, open('static/json/data.json', 'w') as w:
        #     convert(r, w)

        with open('static/json/data.json', newline='') as jsonfile:
            data = json.load(jsonfile)
            return Response(data)
