# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 13:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CheckMyChords', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musicpiece',
            old_name='name',
            new_name='title',
        ),
    ]
