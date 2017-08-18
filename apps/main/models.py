"""MAIN Models - Users"""
from __future__ import unicode_literals
from django.db import models
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #Name and username min. 3 chars
        if len(postData['name']) < 3:
            errors["name"] = "Name must have min. 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username must have min. 3 characters"
        #Make sure that username is not in the database
        findUsers = User.objects.filter(username=postData['username'])
        if len(findUsers) != 0:
            errors["username"] = "username already registered"
        #Password
        if len(postData['password']) < 8:
            errors["password"] = "Password min. 8 chars"
        elif postData['pw_confirm'] != postData['password']:
            errors["pw_confirm"] = "Password must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        #password val
        if len(postData['password']) < 8:
            errors["password"] = "Password min. 8 chars"
        #Username Val
        if len(postData['username']) < 3:
            errors["username"] = "Username must have min. 3 characters"
        else:
            findUsers = User.objects.filter(username=postData['username'])
            if len(findUsers) == 0:
                errors["username"] = "username not registered"
            else:
                if not bcrypt.checkpw(postData['password'].encode("utf8"), findUsers[0].password.encode("utf8")):
                    errors["password"] = "Username and Password do not match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}>".format(self.username)
