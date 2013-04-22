# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Location.neighborhood'
        db.alter_column(u'manticore_tastypie_core_location', 'neighborhood', self.gf('django.db.models.fields.CharField')(max_length=125))

        # Changing field 'Location.name'
        db.alter_column(u'manticore_tastypie_core_location', 'name', self.gf('django.db.models.fields.CharField')(max_length=125))

        # Changing field 'Location.zipcode'
        db.alter_column(u'manticore_tastypie_core_location', 'zipcode', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Location.state'
        db.alter_column(u'manticore_tastypie_core_location', 'state', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Location.address'
        db.alter_column(u'manticore_tastypie_core_location', 'address', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'Location.neighborhood'
        db.alter_column(u'manticore_tastypie_core_location', 'neighborhood', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))

        # Changing field 'Location.name'
        db.alter_column(u'manticore_tastypie_core_location', 'name', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))

        # Changing field 'Location.zipcode'
        db.alter_column(u'manticore_tastypie_core_location', 'zipcode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'Location.state'
        db.alter_column(u'manticore_tastypie_core_location', 'state', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'Location.address'
        db.alter_column(u'manticore_tastypie_core_location', 'address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        u'manticore_tastypie_core.location': {
            'Meta': {'unique_together': "[('name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode')]", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '125'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '125', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'db_index': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['manticore_tastypie_core']