from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}        
        if len(postData['firstname']) < 3:
            errors["firstname"] = "At least 3 characters needed for first name!"       
        if len(postData['lastname']) < 2:
            errors["lastname"] = "At least 3 characters needed for last name!"       
       
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"

        existing_users = User.objects.filter(email=postData['email'])
        if len(existing_users) > 0:
            errors['email2'] = "This email has been used!"

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters!"

        if postData['password'] != postData['confirm']:
            errors["confirm"] = "Password doesn't match!"
        return errors

    def second_validator(self, postData):
        errors = {}
        user = User.objects.get(email=postData['email'])

        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors["password"] = "You can't be logged in!"
        return errors

    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors["destination"] = "Destination can't be empty!"
        if len(postData['description']) < 1:
            errors["description"] = "Desctiption can't be empty!"
        if postData['date_from'] < str(date.today()):
            errors["date_from"] = "Start date can't be in the past!"
        if postData['date_to'] < postData['date_from']:
            errors["date_from"] = "End date must be lafter start date!"

        return errors

class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Trip(models.Model):
    destination = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_from = models.DateField(auto_now=False, auto_now_add=False)
    date_to = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    creator = models.ForeignKey(User, related_name="created_trips")
    joined_users = models.ManyToManyField(User, through='Join', related_name='joined_trips')
    objects = BlogManager()


class Join(models.Model):
    user = models.ForeignKey(User)
    trip = models.ForeignKey(Trip)