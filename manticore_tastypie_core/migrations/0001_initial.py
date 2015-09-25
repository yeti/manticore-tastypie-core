# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default=b'', max_length=125)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('neighborhood', models.CharField(default=b'', max_length=125, db_index=True)),
                ('city', models.CharField(default=b'', max_length=100, db_index=True)),
                ('state', models.CharField(default=b'', max_length=100, db_index=True)),
                ('zipcode', models.CharField(default=b'', max_length=20, db_index=True)),
                ('country_code', models.CharField(max_length=10, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('name', 'neighborhood', 'city', 'state', 'country_code', 'zipcode')]),
        ),
    ]
