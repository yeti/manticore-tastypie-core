# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'manticore_tastypie_core_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=125, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=10, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
        ))
        db.send_create_signal(u'manticore_tastypie_core', ['Location'])

        # Adding unique constraint on 'Location', fields ['name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode']
        db.create_unique(u'manticore_tastypie_core_location', ['name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode'])


    def backwards(self, orm):
        # Removing unique constraint on 'Location', fields ['name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode']
        db.delete_unique(u'manticore_tastypie_core_location', ['name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode'])

        # Deleting model 'Location'
        db.delete_table(u'manticore_tastypie_core_location')


    models = {
        u'manticore_tastypie_core.location': {
            'Meta': {'unique_together': "[('name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode')]", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['manticore_tastypie_core']