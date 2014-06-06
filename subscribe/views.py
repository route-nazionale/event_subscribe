#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.context_processors import csrf
from django.conf import settings
from django.shortcuts import get_object_or_404

from base.models import ScoutChief, Unit, EventHappening
from base.views_support import API_response, API_ERROR_response, HttpJSONResponse
from subscribe.models import ScoutChiefSubscription

from recaptcha.client import captcha

from datetime import *
import json

# simple redirect to landing page
def index(request):
    return redirect('/iscrizione-laboratori/')

# landing page: chief validate through AGESCI code, unit name and birthday
def subscribe(request):

    # if user is logged, redirect to event choose view
    if request.session.get('valid') == True:
        return redirect('/scelta-laboratori/')

    c = {}
    c.update(csrf(request))
    c['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
    c['recaptcha_private_key'] = settings.RECAPTCHA_PRIVATE_KEY
    c['support_email'] = settings.SUPPORT_EMAIL
    return render_to_response('index.html', c)

# API view, used to validate chief
def validate(request):
    if request.method == 'POST':

        # get POST data
        scout_unit = request.POST.get('scout-unit')
        code = request.POST.get('code')
        gg = request.POST.get('gg')
        mm = request.POST.get('mm')
        aaaa = request.POST.get('aaaa')
        recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field')
        recaptcha_response_field = request.POST.get('recaptcha_response_field')

        #STEP 1. SANITIZE ALL INPUT DATA!
        if not gg or not mm or not aaaa:
            return API_ERROR_response(u"Devi inserire la data di nascita")

        try:
            birthday = date(int(aaaa), int(mm), int(gg))
        except ValueError:
            return API_ERROR_response(u"Devi inserire una data di nascita valida (es: 24/09/1991)")
        if not scout_unit:
            return API_ERROR_response(u"Devi inserire il gruppo scout")

        # check captcha
        if not recaptcha_challenge_field:
            return API_ERROR_response(u"RECAPTCHA non inizializzato correttamente")

        if not recaptcha_response_field:
            return API_ERROR_response(u"Devi inserire il codice che leggi nell immagine")

        # talk to the reCAPTCHA service
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META['REMOTE_ADDR'],
        )

        # see if the user correctly entered CAPTCHA information
        # and handle it accordingly.
        if not response.is_valid:
            return API_ERROR_response(u"Il codice che hai ricopiato non è corretto")

        # STEP 2. Query db for extended info

        # check if unit is valid
        if not Unit.objects.filter(name=scout_unit):
            return API_ERROR_response(u"Il gruppo scout che hai inserito non esiste")

        # check AGESCI code
        if not code:
            return API_ERROR_response(u"Devi inserire il codice socio")
        # check if ScoutChief code is valid
        try:
          chief = ScoutChief.objects.get(code=code)
        except ScoutChief.DoesNotExist:
            return API_ERROR_response(u"Il codice socio che hai inserito non esiste")
        # check if ScoutChief is in the correct Unit
        if chief.scout_unit.name != scout_unit:
            return API_ERROR_response(u"Il codice che hai fornito risulta censito in un altro gruppo")

        # check birthday
        if chief.birthday != birthday:
            return API_ERROR_response(u"La data di nascita inserita non corrisponde con quella del codice socio")

        # check if chief is_spalla
        if chief.is_spalla:
            return API_ERROR_response(u"Risulti essere un capo spalla, verrai iscritto dalla Pattuglia Eventi. Per info %s" % settings.SUPPORT_EMAIL)

        # chief is valid
        request.session['valid'] = True
        request.session['chief_code'] = code
        return API_response()

    # method is GET
    else:
        raise PermissionDenied

# validated chief view and subscribe to events
def choose(request):
    if not 'valid' in request.session or not request.session['valid']:
        return redirect('/iscrizione-laboratori/')
    else:
        chief = ScoutChief.objects.get(code=request.session['chief_code'])
        c = {}
        c.update(csrf(request))
        c['chief'] = {}
        c['chief']['code'] = chief.code
        c['chief']['name'] = chief.name
        c['chief']['surname'] = chief.surname
        c['chief']['group'] = chief.scout_unit.name
        return render_to_response('choose.html', c)

# logout view
def logout(request):
    if 'valid' in request.session:
        request.session['valid'] = False
        request.session['chief_code'] = None

    return redirect('/iscrizione-laboratori/')

# subscribe API view
def event_subscribe(request, happening_id):

    if request.method == "POST":
        if request.session.get('valid') == True:
            rv = API_ERROR_response(u'non hai effettuato il login')
        else:
            chief = ScoutChief.objects.get(code=request.session['chief_code'])
            if chief.is_spalla:
                rv = API_ERROR_response(
                    u"Sei un capo spalla, come sei arrivato fin qui? Prego contattare %s" % settings.SUPPORT_EMAIL
                )
            else:
                eh = get_object_or_404(EventHappening, pk=happening_id)
                subscription = ScoutChiefSubscription(scout_chief=chief, event_happening=eh)
                try:
                    subscription.save()
                except ValidationError as e:
                    rv = API_ERROR_response(unicode(e))
                rv = API_response()
    else:
        raise PermissionDenied

    return rv

def event_unsubscribe(request, happening_id):

    if request.method == "POST":
        if request.session.get('valid') == True:
            rv = API_ERROR_response(u'non hai effettuato il login')
        else:
            chief = ScoutChief.objects.get(code=request.session['chief_code'])
            if chief.is_spalla:
                rv = API_ERROR_response(
                    u"Sei un capo spalla, come sei arrivato fin qui? Prego contattare %s" % settings.SUPPORT_EMAIL
                )
            else:
                eh = get_object_or_404(EventHappening, pk=happening_id)
                subscription = get_object_or_404(ScoutChiefSubscription, scout_chief=chief, event_happening=eh)
                try:
                    subscription.delete()
                except ValidationError as e:
                    rv = API_ERROR_response(unicode(e))
                else:
                    rv = API_response()
    else:
        raise PermissionDenied

    return rv

#--------------------------------------------------------------------------------

def myevents(request):

    chief_code = request.session['chief_code']
    scout_chief = get_object_or_404(ScoutChief, code=chief_code)
    if scout_chief.is_spalla:
        rv = API_ERROR_response(
            u"Sei un capo spalla, come sei arrivato fin qui? Prego contattare %s" % settings.SUPPORT_EMAIL
        )
    else:

        eh_qs = EventHappening.objects.filter(
            scoutchiefsubscription__scout_chief=scout_chief
        )
        rv = HttpJSONResponse(map(lambda x: x.as_dict(), eh_qs))

    return rv
    

