from django.shortcuts import render
from base.models import Event, Unit
from django.core import serializers
from django.http import HttpResponse

import json

def events(request):
    events_as_json = serializers.serialize('json', Event.objects.all())
    return HttpResponse(events_as_json, content_type="application/json")

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpResponse(json.dumps(units), content_type="application/json")
