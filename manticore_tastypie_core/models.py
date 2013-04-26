from django.db import models
from manticore_django.manticore_django.models import CoreModel
from manticore_tastypie_social.manticore_tastypie_social.models import FollowableModel

__author__ = 'rudolphmutter'


# Postgres doesn't include nulls in unique constraints, entering empty strings for default to protect duplicate locations
class Location(CoreModel):
    FIELDS_TO_FILTER = ['name', 'neighborhood', 'city', 'state', 'country_code']

    name = models.CharField(max_length=125, default='')
    latitude = models.FloatField()
    longitude = models.FloatField()
    neighborhood = models.CharField(max_length=125, default='', db_index=True)
    city = models.CharField(max_length=100, db_index=True, default='')
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

    # Take available fields on the location object and turn them into filters
    def containing_filters(self):
        filters = {}
        for FIELD in self.FIELDS_TO_FILTER:
            value = getattr(self, FIELD)
            if value and value != '':
                filters["location__%s" % FIELD] = value
        return filters

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.country_code = self.country_code.upper()
        super(Location, self).save(force_insert, force_update, using, update_fields)

FollowableModel.register(Location)