from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.conf import settings
from base.models import ScoutChief, Unit

from recaptcha.client import captcha

# simple redirect to landing page
def index(request):
    return redirect('/iscrizione-laboratori/')

# landing page: chief validate through AGESCI code, unit name and birthday
def subscribe(request):
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
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il gruppo scout"}')
        # check if unit is valid
        if not Unit.objects.filter(name=scout_unit):
            return HttpResponse('{"status": "ERROR", "message": "Il gruppo scout che hai inserito non esiste"}')

        # check AGESCI code
        if not code:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il codice socio"}')
        # check if ScoutChief code is valid
        if not ScoutChief.objects.filter(code=code):
            return HttpResponse('{"status": "ERROR", "message": "Il codice socio che hai inserito non esiste"}')
        # check if ScoutChief is in the correct Unit
        if not ScoutChief.objects.filter(scout_unit=scout_unit, code=code):
            return HttpResponse('{"status": "ERROR", "message": "Il codice che hai fornito risulta censito in un altro gruppo"}')

        # check birthday
        if not gg or not mm or not aaaa:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire la data di nascita"}')

        # check captcha
        if not recaptcha_challenge_field:
            return HttpResponse('{"status": "ERROR", "message": "RECAPTCHA non inizializzato correttamente"}')

        if not recaptcha_response_field:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il codice che leggi nell immagine"}')

        # talk to the reCAPTCHA service
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META['REMOTE_ADDR'],)

        # see if the user correctly entered CAPTCHA information
        # and handle it accordingly.
        if not response.is_valid:
            return HttpResponse('{"status": "ERROR", "message": "Il codice che hai ricopiato non e corretto"}')

        # chief is valid
        request.session['valid'] = True
        request.session['chief_code'] = code
        return HttpResponse('{"status": "OK"}')

    # method is GET
    else:
        return HttpResponse('')

# validated chief view and subscribe to events
def choose(request):
    if not 'valid' in request.session or not request.session['valid']:
        return redirect('/iscrizione-laboratori/')
    else:
        chief = ScoutChief.objects.get(code=request.session['chief_code'])
        c = {}
        c['chief_code'] = chief.code
        c['chief_group'] = chief.scout_unit.name
        return render_to_response('choose.html', c)
