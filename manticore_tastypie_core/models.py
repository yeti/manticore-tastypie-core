from django.db import models
from manticore_django.manticore_django.models import CoreModel
from manticore_tastypie_social.manticore_tastypie_social.models import FollowableModel

__author__ = 'rudolphmutter'


class Location(CoreModel):
    # Google Place unique ID
    id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=125, null=True, blank=True)
    address = models.CharField(max_length=125, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=40)

    def __unicode__(self):
        return u"%s" % self.name

    def identifier(self):
        return u"%s" % self.name

FollowableModel.register(Location)