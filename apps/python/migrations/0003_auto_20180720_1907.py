# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-20 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('python', '0002_trip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='python.Trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='python.User')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='joined_users',
            field=models.ManyToManyField(related_name='joined_trips', through='python.Join', to='python.User'),
        ),
    ]
