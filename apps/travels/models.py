# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..main.models import User
from datetime import datetime

# Create your models here.


class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        flag = False
        #No empty entries
        if len(postData['destination']) < 1:
            flag = True
            errors["destination"] = "Destination required"

        if len(postData['desc']) < 1:
            flag = True
            errors["desc"] = "Description required"

        #Both dates must be in the future
        try:  # Start Date try/except
            start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
            if start_date < datetime.today():
                flag = True
                errors["start_date"] = "Travel Date From: must be in the future"
        except ValueError:
            flag = True
            errors["start_date"] = "Travel Date From: Input Valid Date"
        
        try:#End Date try/except
            end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
            if end_date < datetime.today(): #OOPS
                flag = True
                errors["end_date"] = "Travel Date To: must be in the future"
        except ValueError:
            flag = True
            errors["end_date"] = "Travel Date To: Input Valid Date"
        
        #Start Date must be before end date
        if not flag:
            if start_date > end_date:
                errors["end_date"] = "Start date must be before end date"
        return errors

class Trip(models.Model):
    planner = models.ForeignKey(User, related_name="trips")
    users = models.ManyToManyField(User, related_name="schedule")
    destination = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __repr__(self):
        return "<Trip object: {}>".format(self.destination)
