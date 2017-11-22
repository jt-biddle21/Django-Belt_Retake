from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
import datetime


class Manager(models.Manager):
    def basic_validator(self, postData, type):
        if type == "Register":
            errors = []
            if postData['datehired'] == "":
                errors.append("Please enter in the date you were hired")
            else:
                datehire = datetime.datetime.strptime(postData['datehired'], "%Y-%m-%d")
                if datehire > datetime.datetime.today():
                    errors.append('Please enter a valid date either today or earlier')
            if len(postData['name']) < 3:
                errors.append("You need to enter in a first name!")
            if len(postData['username']) < 3:
                errors.append("You need to enter in a username!")
            if len(postData['password']) < 8:
                errors.append("You need to enter in a password 8 characters or longer!")
            if postData['confirmpw'] != postData['password']:
                errors.append("Your passwords do not match!")
            if len(errors) > 0:
                return errors
            elif len(errors) == 0:
                hashpass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt(5))
                new_user = User.objects.create(name=postData['name'], username=postData['username'], password=hashpass, datehired=postData['datehired'])
                return new_user
        if type == "Login":
            lerrors = []
            if len(User.objects.filter(username=postData['Logusername'])) > 0:
                user = User.objects.filter(username=postData['Logusername'])[0]
                if not bcrypt.checkpw(postData['Logpassword'].encode(), user.password.encode()):
                    lerrors.append("Incorrect username or password")
                    return lerrors
            elif len(User.objects.filter(username=postData['Logusername'])) == 0:
                lerrors.append("Incorrect username or password")
                return lerrors
            return user
        if type == "NewItem":
            perrors = []
            if postData['newitem'] == "":
                perrors.append("You need to enter an item!")
            if len(perrors) > 0:
                return perrors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    datehired = models.DateField(null=True)
    objects = Manager()

    def __repr__(self):
        return "<User Object: {} {} {} {}>".format(self.name, self.username, self.password, self.datehired)


class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    dateadded = models.DateTimeField(auto_now_add=True)
    users = models.ForeignKey(User, related_name="items")
    wishedby = models.ManyToManyField(User, related_name="wishes")

    def __repr__(self):
        return "<User Object: {} {}>".format(self.item, self.dateadded)
