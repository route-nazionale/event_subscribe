from django.shortcuts import render
from base.models import Event, Unit
from django.http import HttpResponse

import json

def events(request):
    fields_to_serialize = [
            "max_age",
            "kind",
            "state_subscription",
            "state_chief",
            "name",
          #"district", added manually
            "max_chiefs_seats",
            "min_age",
          #"topic", added manually
            "max_boys_seats",
            "state_activation",
            "num",
            "min_seats",
            "seats_n_chiefs",
            "seats_n_boys",
            "seats_tot",
            "state_handicap",
            "description",
            "code",            # this is a proprety
            "n_seats",         # this is a proprety
            "available_seats", # this is a proprety
    ]
    events = []
    for event in Event.objects.all():
        obj = {}
        for field in fields_to_serialize:
          obj[field] = getattr(event, field)
        obj['topic'] = event.topic.code
        obj['district'] = event.district.code
        events.append(obj)
    return HttpResponse(json.dumps(events), content_type="application/json")

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpResponse(json.dumps(units), content_type="application/json")
