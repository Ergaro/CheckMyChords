# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CheckMyChords', '0003_musicpiece_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicpiece',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
