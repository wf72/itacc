# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0003_auto_20150316_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='login',
            field=models.CharField(default=datetime.datetime(2015, 3, 17, 10, 0, 9, 472392, tzinfo=utc), unique=True, max_length=30),
            preserve_default=False,
        ),
    ]
