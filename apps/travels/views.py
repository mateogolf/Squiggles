"""TRAVELS VIEWS"""
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from ..main.models import User


def index(request):
    #Find name of user with
    user = User.objects.get(id=request.session['id'])
    context = {
        'name': user.name,
        'schedule': user.schedule.all(),
        'other_trips': Trip.objects.exclude(users=user)
    }
    # #Get all user's schedule
    # if 'schedule' not in request.session:
    #     request.session['schedule'] = []

    # schedule = user.schedule.all()
    # # users = trip.users.exclude(id=trip.planner.id)
    # for trip in schedule:
    #     request.session['schedule'].append(trip)

    # #Get all other schedules
    # if 'other_trips' not in request.session:
    #     request.session['other_trips'] = []
    # # trips = Trip.objects.all()
    # # print trips
    # # trips = User.objects.all().schedule.trips.exclude(user_id=request.session['id'])
    # trips = Trip.objects.exclude(users=user)
    # for other in trips:
    #     request.session['other_trips'].append(other)

    return render(request, 'travels/index.html', context)


def new(request):  # /add
    return render(request, 'travels/edit.html')


def create(request):  # /create
    if request.method == "POST":
        #Validate
        errors = Trip.objects.basic_validator(request.POST)
        if len(errors):
            context = {
                'destination': request.POST['destination'],
                'desc': request.POST['desc'],
                'start_date': request.POST['start_date'],
                'end_date': request.POST['end_date'],
            }
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
                print tag + ": " + error
            return render(request, 'travels/edit.html', context)
        else:
            user = User.objects.get(id=request.session['id'])
            #Create Trip
            newTrip = Trip(
                destination=request.POST['destination'],
                desc=request.POST['desc'],
                planner=user,
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'])
            #Add User to users
            newTrip.save()
            newTrip.users.add(user)
            return redirect('/travels')
    else:
        return redirect('/travels')


def show(request, trip_id):  # /destination/trip_id
    #Get trip
    trip = Trip.objects.get(id=trip_id)
    context = {
        'planner': trip.planner,
        'destination': trip.destination,
        'desc': trip.desc,
        'start_date': trip.start_date,
        'end_date': trip.end_date,

    }
    #get trip's users, filter out planner
    users = trip.users.exclude(id=trip.planner.id)
    print users
    #assign users to request.sessions['users']
    if 'users' not in request.session:
        request.session['users'] = []
    for user in users:
        request.session['users'].append(user.name)
    return render(request, 'travels/trip.html', context)


def addSchedule(request, trip_id):  # "/travels/{{trip.id}}"
    user = User.objects.get(id=request.session['id'])
    findUsers = user.schedule.filter(id=trip_id)
    if len(findUsers) != 0:
        messages.error(request, "Already Joined this one")
        return redirect('/travels')
    else:
        #Get logged in user
        user = User.objects.get(id=request.session['id'])
        user.schedule.add(Trip.objects.get(id=trip_id))
        user.save()
        return redirect('/travels')
