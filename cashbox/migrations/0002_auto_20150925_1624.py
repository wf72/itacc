# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashboxcardselection',
            name='id',
            field=models.SmallIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='cashboxsectionselection',
            name='id',
            field=models.SmallIntegerField(serialize=False, primary_key=True),
        ),
    ]
