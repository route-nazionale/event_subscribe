from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse

def index(request):
    return redirect('/iscrizione-laboratori/')

def subscribe(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c)

def choose(request):
    return render_to_response('choose.html')

def validate(request):
    if request.method == 'POST':
       
        # get POST data 
        scout_unit = request.POST.get('scout-unit')
        code = request.POST.get('code')
        birthday = request.POST.get('birthday')
        captcha = request.POST.get('captcha') 

        # check scout_unit
        if not scout_unit:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il gruppo scout"}')

        # check code
        if not code:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il codice socio"}')

        # check birthday
        if not birthday:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire la data di nascita"}')         

        # check birthday
        if not captcha:
            return HttpResponse('{"status": "ERROR", "message": "Devi inserire il codice che leggi nell immagine"}')

        # chief is valid
        return HttpResponse('{"status": "OK"}')

    else:
        return HttpResponse('')
    
