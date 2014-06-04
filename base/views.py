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

def myevents(request):
    events = []
    #eh_qs = EventHappening.objects.distinct('timeslot')[:3] #DO NOT WORK ON SQLITE
    my_first_eh = EventHappening.objects.all()[0]
    eh_qs = EventHappening.objects.filter(pk=my_first_eh.pk) 
    eh_qs |= EventHappening.objects.exclude(timeslot=my_first_eh.timeslot)
    for eh in eh_qs[:2]:
        obj = eh.as_dict()
        events.append(obj)
    return HttpJSONResponse(events)
    

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)
