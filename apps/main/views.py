"""MAIN VIEWS.py"""
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
# Create your views here.
def index(request):
    if 'id' in request.session:
        request.session.clear()
    return render(request, 'main/index.html')

def register(request):
    if request.method == "POST":
        #Validate
        errors = User.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for tag, error in errors.iteritems():#flash messages
                messages.error(request, error, extra_tags=tag)
            #context name username
            context = {
                'name': request.POST['name'],
                'username': request.POST['username']
            }
            return render(request, 'main/index.html',context)
        else:
            #Hash password
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            #Create User(key=request.POST['key'])
            newUser = User(
                name=request.POST['name'],
                username=request.POST['username'],
                password=hash1)
            newUser.save()
            request.session['id'] = User.objects.get(username=request.POST['username']).id
            return redirect('/travels')
    else:
        return redirect('/main')


def login(request):
    if request.method == "POST":
        #Validate
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for tag, error in errors.iteritems():#flash messages
                messages.error(request, error, extra_tags=tag)
            context = {
                'lusername': request.POST['username']
            }
            return render(request, 'main/index.html',context)
        else:
            request.session['id'] = User.objects.get(username=request.POST['username']).id
            return redirect('/travels')
    else:
        return redirect('/main')

def success(request):
    #Find name of user with 
    user = User.objects.get(id=request.session)
    context = {'name': user.name}
    return render(request,'/travels',context)
