# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('addressbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldap_settings',
            name='active',
            field=models.BooleanField(default=b'False', unique=True),
            preserve_default=True,
        ),
    ]
