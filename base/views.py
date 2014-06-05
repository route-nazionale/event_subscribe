from django.shortcuts import render
from django.db import models

from base.models import EventHappening, Unit
from base.views_support import HttpJSONResponse


def events(request):
    events = []
    for eh in EventHappening.objects.all():
        obj = eh.as_dict()
        events.append(obj)
    return HttpJSONResponse(events)

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)
