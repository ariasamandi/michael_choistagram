# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt
from models import *
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import Image
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = []
        print postData
        if len(postData['first_name']) < 3:
            errors.append('First name must be 3 or more characters')
        if len(postData['last_name']) < 3:
            errors.append('last name must be 3 or more characters')
        if len(postData['username']) < 3:
            errors.append('username must be 3 or more characters')
        if len(postData['password']) < 8:
            errors.append('password must be 8 or more characters')
        if len(postData['password']) != len(postData['confirm_password']):
            errors.append('passwords do not match')
        if len(User.objects.filter(username = postData['username'])) > 0:
            errors.append("Username already taken!")
        if len(errors) > 0:
            return {"errors": errors}
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            the_user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], username = postData['username'], post_tokens = 5, password = hashed_pw)
            return {"user": the_user}
    def login_validator(self, postData):
        errors = []
        try:
            the_user = User.objects.get(username=postData['username'])
            print the_user
        except:
            print "error"
            errors.append("Username or password invalid")
            return {"errors": errors}
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            print "it worked"
            return {"user": the_user}
        errors.append("Username or password invalid")
        return {"errors": errors}

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    post_tokens = models.IntegerField()
    friends = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Post(models.Model):
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(source='image',processors=[ResizeToFill(350, 200)], format='JPEG', options={'quality': 60})
    posted_by = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
