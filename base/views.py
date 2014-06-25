from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db import models

from base.models import EventHappening, Unit, Event, ScoutChief
from base.views_support import HttpJSONResponse, API_ERROR_response

from django.views.decorators.cache import cache_page
from django.conf import settings

from django.db import connection, reset_queries


@cache_page(settings.CACHE_EXPIRE_TIME) # seconds
def events(request):
    """
    Return all subscriptable events.

    """
    reset_queries()
    '''
    #NOTE: weird login check... as usual unfortunately
    if not request.session.get('valid'):
        rv = API_ERROR_response(u'non hai effettuato il login')
    else:

        events = []
        # Restrict to those enabled or reserved for chiefs
        eh_qs = EventHappening.objects.filter(event__state_chief__in=(Event.STATE_ENABLED, Event.STATE_RESERVED))
        # Restrict to those actives
        eh_qs = eh_qs.filter(event__state_activation=Event.ACTIVATION_ACTIVE)
        # Restrict to those open for subscription
        eh_qs = eh_qs.filter(event__state_subscription=Event.SUBSCRIPTION_OPEN)
        for eh in eh_qs:
            # Restrict to those with available seats
            # I use properties here, cannot filter in QuerySet!
            if eh.available_seats:
                obj = eh.as_dict()
                events.append(obj)
        
        rv = HttpJSONResponse(events)
    '''
    a = EventHappening.objects.all()
    for q in connection.queries:
        print q

    return HttpResponse(a)


def units(request):

    # Units autocompletion -> no login required
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)
