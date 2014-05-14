from django.shortcuts import render
from base.models import Event
from django.core import serializers
from django.http import HttpResponse

def events(request):
    events_as_json = serializers.serialize('json', Event.objects.all())
    return HttpResponse(events_as_json, content_type="application/json")
