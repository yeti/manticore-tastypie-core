from django.db import models
from manticore_django.manticore_django.models import CoreModel
from manticore_tastypie_social.manticore_tastypie_social.models import FollowableModel

__author__ = 'rudolphmutter'


# Postgres doesn't include nulls in unique constraints, entering empty strings for default to protect duplicate locations
class Location(CoreModel):
    name = models.CharField(max_length=125, default='')
    address = models.CharField(max_length=200, default='')
    latitude = models.FloatField()
    longitude = models.FloatField()
    neighborhood = models.CharField(max_length=125, default='', db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=30, db_index=True, default='')
    zipcode = models.CharField(max_length=10, db_index=True, default='')
    country_code = models.CharField(max_length=10, db_index=True)

    class Meta:
        unique_together = [('name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode')]

    def __unicode__(self):
        return u"%s" % self.name

    def identifier(self):
        if not self.name or self.name == '':
            return u"%s" % self.city
        else:
            return u"%s" % self.name

FollowableModel.register(Location)