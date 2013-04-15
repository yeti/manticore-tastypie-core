from django.db import models
from manticore_django.manticore_django.models import CoreModel

__author__ = 'rudolphmutter'


class Location(CoreModel):
    # Google Place unique ID
    id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=125)
    address = models.CharField(max_length=125)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return u"%s" % self.name