from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def index(request):
    return redirect('/iscrizione-laboratori/')

def subscribe(request):
    return HttpResponse('Welcome')
