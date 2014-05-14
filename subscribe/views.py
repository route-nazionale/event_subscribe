from django.shortcuts import render, redirect, render_to_response

def index(request):
    return redirect('/iscrizione-laboratori/')

def subscribe(request):
    return render_to_response('index.html')

def choose(request):
    return render_to_response('choose.html')
