from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'python/index.html')

def register(request):

    errors = User.objects.basic_validator(request.POST)
 
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(firstname=request.POST['firstname'], lastname=request.POST['lastname'],email=request.POST['email'], password= hashed )

        return redirect('/success')

def success(request):

    return render(request, 'python/success.html')

def validate(request):
    errors = User.objects.second_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['firstname'] = User.objects.get(email=request.POST['email']).firstname
        request.session['id'] = User.objects.get(email=request.POST['email']).id

        return redirect('/travels')

def travels(request):
    joined_trips = User.objects.get(id=request.session['id']).joined_trips.all()
    context = {
        "self_created_trips": User.objects.get(id=request.session['id']).created_trips.all(),
        "other_created_trips": Trip.objects.exclude(creator_id=request.session['id']),
        "joined_trips": User.objects.get(id=request.session['id']).joined_trips.all(),
        "other_trips": Trip.objects.exclude(creator_id=request.session['id']).exclude(joined_users=request.session['id'])
    }

    return render(request, 'python/travels.html', context)

def addtrip(request):

    return render(request, 'python/addtrip.html')

def add_a_trip(request):

    errors = Trip.objects.trip_validator(request.POST)
 
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    else:
        new_trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], date_from = request.POST['date_from'], date_to = request.POST['date_to'], creator_id = request.session['id'])
        # new_join = Join.objects.create(trip_id=new_trip.id, user_id=request.session['id'])
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def this_trip(request, id):
    context = {
        "trip": Trip.objects.get(id=id),
        "joined_users": Trip.objects.get(id=id).joined_users.all()
    }
    return render(request, 'python/this_trip.html', context)

def join_trip(request, id):
    if len(Join.objects.filter(trip_id=id, user_id = request.session['id'])) > 0:
        return redirect('/travels')
    else:
        new_join = Join.objects.create(trip_id=id, user_id = request.session['id'])

        return redirect('/travels')

def cancel_trip(request, id):

    j = Join.objects.get(trip_id = id, user_id = request.session['id'])
    j.delete()

    return redirect('/travels')

def delete_trip(request, id):

    t = Trip.objects.get(id = id)
    t.delete()

    return redirect('/travels')