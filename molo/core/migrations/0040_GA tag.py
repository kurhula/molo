# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-20 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_add content rotation to SectionPage'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='global_ga_tag',
            field=models.CharField(blank=True, help_text='Global GA Tag tracking code to be used to view analytics on more than one site globally', max_length=255, null=True, verbose_name='Global GA Tag Manager'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='local_ga_tag',
            field=models.CharField(blank=True, help_text='Local GA Tag tracking code to be used to view analytics on this site only', max_length=255, null=True, verbose_name='Local GA Tag Manager'),
        ),
    ]
