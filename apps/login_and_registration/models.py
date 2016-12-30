from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
import bcrypt
import re

from django.core.validators import RegexValidator

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'[a-zA-Z-]*[a-zA-Z-]+[a-zA-Z-]$')

class UserManager(models.Manager):
    def reg_validation(self, request):
        errors = []
        if not request.POST['first_name'] or not request.POST['last_name']:
            errors.append('- Both First and Last Name are required!')
        if len(request.POST['first_name']) < 2:
            errors.append('- First Name must be 2 or more characters!')
        if len(request.POST['last_name']) < 2:
            errors.append('- Last Name must be 2 or more characters!')
        if not NAME_REGEX.match(request.POST['first_name']) or not NAME_REGEX.match(request.POST['last_name']):
            errors.append('- Both First and Last Name must consist only of alpha characters (dash OK)')
        if len(request.POST['alias']) < 3:
            errors.append('- Alias must be at least 2 characters')
        if not request.POST['email']:
            errors.append('- Email is required!')
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append('- Email entered is invalid format - s/b: xxxx@xxxx.xxx')
        if len(request.POST['password']) < 8:
            errors.append('- Password must be at least 8 characters')
        if request.POST['password'] != request.POST['confirm_password']:
            errors.append('- Passwords must match!')
        if not errors:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = self.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                alias=request.POST['alias'],
                email=request.POST['email'],
                password=pw_hash,
            )
            return (True, user)
        else:
            print errors
            return (False, errors)

    def login_validation(self, request):
        errors = []
        try:
            user = User.objects.get(email=request.POST['email'])

            hashed = User.objects.get(email=request.POST['email']).password
            hashed = hashed.encode('utf-8')
            password = request.POST['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
            # password = request.POST['password'].encode()
                # print user.id, password
            # if bcrypt.hashpw(password, user.password.encode()):
                # print 'hashed: ', hashed
                return (True, user)
            else:
                errors.append('- Incorrect Email and/or Password')
                return (False, errors)
        except:
            errors.append('- Incorrect Email and/or Password')
            return (False, errors)

    def update_user(self, id, request):
        user = User.objects.get(id=id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.alias = request.POST['alias']
        user.email = request.POST['email']
        user.save()


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    alias = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()