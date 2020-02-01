from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
import json
from .load_data import *
from gcmf.load_data import *


def overview(request):
    if request.method == "GET":
        return render(request, 'pipeline/index.html', context={})

    if request.method == "POST":
        if request.POST.get('action') == 'load_data':
            load_periods()
            load_rbs()
            load_countries()
            load_wbs()
            load_commodities()
            load_supply_lines()
            load_corridors()
            load_gcmf_commodities()
            load_pipeline()

            return HttpResponse(json.dumps({}), content_type='application/json')


