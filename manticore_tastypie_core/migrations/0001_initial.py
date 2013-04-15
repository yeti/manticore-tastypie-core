# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'manticore_tastypie_core_location', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'manticore_tastypie_core', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'manticore_tastypie_core_location')


    models = {
        u'manticore_tastypie_core.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        }
    }

    complete_apps = ['manticore_tastypie_core']