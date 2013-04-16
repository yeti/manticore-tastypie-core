# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.city'
        db.add_column(u'manticore_tastypie_core_location', 'city',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Location.state'
        db.add_column(u'manticore_tastypie_core_location', 'state',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.zipcode'
        db.add_column(u'manticore_tastypie_core_location', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.country'
        db.add_column(u'manticore_tastypie_core_location', 'country',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40),
                      keep_default=False)


        # Changing field 'Location.name'
        db.alter_column(u'manticore_tastypie_core_location', 'name', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))

        # Changing field 'Location.address'
        db.alter_column(u'manticore_tastypie_core_location', 'address', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))

    def backwards(self, orm):
        # Deleting field 'Location.city'
        db.delete_column(u'manticore_tastypie_core_location', 'city')

        # Deleting field 'Location.state'
        db.delete_column(u'manticore_tastypie_core_location', 'state')

        # Deleting field 'Location.zipcode'
        db.delete_column(u'manticore_tastypie_core_location', 'zipcode')

        # Deleting field 'Location.country'
        db.delete_column(u'manticore_tastypie_core_location', 'country')


        # Changing field 'Location.name'
        db.alter_column(u'manticore_tastypie_core_location', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=125))

        # Changing field 'Location.address'
        db.alter_column(u'manticore_tastypie_core_location', 'address', self.gf('django.db.models.fields.CharField')(default='', max_length=125))

    models = {
        u'manticore_tastypie_core.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['manticore_tastypie_core']