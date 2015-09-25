# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashbox', '0004_auto_20150925_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbox',
            name='settings',
            field=models.ForeignKey(to='cashbox.CashBoxSetting'),
        ),
    ]
