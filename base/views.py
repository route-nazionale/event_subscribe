from django.shortcuts import render
from django.db import models

from base.models import EventHappening, Unit
from base.views_support import HttpJSONResponse

import json, datetime

def events(request):
    fields_to_serialize = [
        "id",
        "timeslot",
        "max_age",
        "kind",
        "state_subscription",
        "state_chief",
        "name",
        "district", #added manually
        "max_chiefs_seats",
        "min_age",
        "topic", #added manually
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
        "dt_start", "dt_stop",
    ]
    events = []
    for event in EventHappening.objects.all():
        obj = {}
        for field in fields_to_serialize:
            v = getattr(event, field)
            if isinstance(v, (models.Field, models.Model)):
                v = unicode(v)
            elif isinstance(v, datetime.datetime):
                v = v.strftime("%s")
            obj[field] = v
        obj['happening_id'] = event.pk
        events.append(obj)
    return HttpJSONResponse(events)

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)
