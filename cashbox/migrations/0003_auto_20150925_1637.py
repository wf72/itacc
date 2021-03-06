# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashbox', '0002_auto_20150925_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashboxsetting',
            name='vibor_sekcii',
            field=models.SmallIntegerField(default=0, choices=[(0, b'\xd0\x92\xd1\x81\xd0\xb5 \xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8 \xd0\xb2 \xd0\xbe\xd0\xb4\xd0\xbd\xd1\x83 \xd1\x81\xd0\xb5\xd0\xba\xd1\x86\xd0\xb8\xd1\x8e'), (1, b'\xd0\xa2\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xba\xd0\xbe \xd0\xbf\xd1\x80\xd0\xb8 \xd1\x81\xd0\xb2\xd0\xbe\xd0\xb1\xd0\xbe\xd0\xb4\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x86\xd0\xb5\xd0\xbd\xd0\xb5'), (2, b'\xd0\x95\xd1\x81\xd0\xbb\xd0\xb8 \xd0\xbd\xd0\xb5 \xd1\x83\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0\xd0\xbd\xd0\xb0 \xd1\x81\xd0\xb5\xd0\xba\xd1\x86\xd0\xb8\xd1\x8f'), (3, b'\xd0\x9f\xd1\x80\xd0\xb8 \xd0\xba\xd0\xb0\xd0\xb6\xd0\xb4\xd0\xbe\xd0\xb9 \xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8'), (4, b'\xd0\x9f\xd0\xbe \xd1\x81\xd0\xb2\xd0\xbe\xd0\xb1\xd0\xbe\xd0\xb4\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x86\xd0\xb5\xd0\xbd\xd0\xb5 \xd0\xb2 \xd0\xbe\xd0\xb4\xd0\xbd\xd1\x83 \xd1\x81\xd0\xb5\xd0\xba\xd1\x86\xd0\xb8\xd1\x8e')]),
        ),
    ]
