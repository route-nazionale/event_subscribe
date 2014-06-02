#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.conf import settings
from base.models import ScoutChief, Unit

from recaptcha.client import captcha

from datetime import *
import json

# simple redirect to landing page
def index(request):
    return redirect('/iscrizione-laboratori/')

# landing page: chief validate through AGESCI code, unit name and birthday
def subscribe(request):

    # if user is logged, redirect to event choose view
    if request.session.get('valid'):
        return redirect('/scelta-laboratori/')

    c = {}
    c.update(csrf(request))
    c['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
    c['recaptcha_private_key'] = settings.RECAPTCHA_PRIVATE_KEY
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

        # check scout_unit
        if not scout_unit:
            return API_response("ERROR", "Devi inserire il gruppo scout")
        # check if unit is valid
        if not Unit.objects.filter(name=scout_unit):
            return API_response("ERROR", "Il gruppo scout che hai inserito non esiste")

        # check AGESCI code
        if not code:
            return API_response("ERROR", "Devi inserire il codice socio")
        # check if ScoutChief code is valid
        try:
          chief = ScoutChief.objects.get(code=code)
        except ScoutChief.DoesNotExist:
            return API_response("ERROR", "Il codice socio che hai inserito non esiste")
        # check if ScoutChief is in the correct Unit
        if chief.scout_unit.name != scout_unit:
            return API_response("ERROR", "Il codice che hai fornito risulta censito in un altro gruppo")

        # check birthday
        if not gg or not mm or not aaaa:
            return API_response("ERROR", "Devi inserire la data di nascita")

        try:
            birthday = date(int(aaaa), int(mm), int(gg))
        except ValueError:
            return API_response("ERROR", "Devi inserire una data di nascita valida (es: 24/09/1991)")

        if chief.birthday != birthday:
            return API_response("ERROR", "La data di nascita inserita non corrisponde con quella del codice socio")

        # check captcha
        if not recaptcha_challenge_field:
            return API_response("ERROR", "RECAPTCHA non inizializzato correttamente")

        if not recaptcha_response_field:
            return API_response("ERROR", "Devi inserire il codice che leggi nell immagine")

        # talk to the reCAPTCHA service
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META['REMOTE_ADDR'],)

        # see if the user correctly entered CAPTCHA information
        # and handle it accordingly.
        if not response.is_valid:
            return API_response("ERROR", "Il codice che hai ricopiato non è corretto")

        # chief is valid
        request.session['valid'] = True
        request.session['chief_code'] = code
        return API_response("OK")

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

# subscribe and unsubscribe API view
def event(request, event_code, action):
    if not 'valid' in request.session or not request.session['valid']:
        API_response('ERROR', 'non hai effettuato il login')

    return API_response('OK')

# create a JSON response to POST
def API_response(status, message=''):
    response = {}
    response['status'] = status
    response['message'] = message
    return HttpResponse(json.dumps(response), content_type="application/json")
