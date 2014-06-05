from django.shortcuts import render
from django.db import models

from base.models import EventHappening, Unit, Event
from base.views_support import HttpJSONResponse


def events(request):
    events = []
    eh_qs = EventHappening.objects.all()
    eh_qs = eh_qs.filter(event__state_chief__in=(Event.STATE_ENABLED, Event.STATE_RESERVED))
    eh_qs = eh_qs.filter(event__state_activation=Event.ACTIVATION_ACTIVE)
    eh_qs = eh_qs.filter(event__state_subscription=Event.SUBSCRIPTION_OPEN)
    for eh in eh_qs:
        obj = eh.as_dict()
        events.append(obj)
    return HttpJSONResponse(events)

def units(request):
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)
