# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('fathername', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('cellphone', models.CharField(max_length=200)),
                ('address', models.TextField(max_length=300)),
                ('email', models.EmailField(max_length=75)),
                ('photo', models.ImageField(upload_to=b'')),
                ('birthday', models.DateField()),
                ('active', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
