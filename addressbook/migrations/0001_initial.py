# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lastname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('fathername', models.CharField(max_length=200, blank=True)),
                ('company', models.CharField(max_length=200, blank=True)),
                ('position', models.CharField(max_length=200, blank=True)),
                ('department', models.CharField(max_length=200, blank=True)),
                ('phone', models.CharField(max_length=200, blank=True)),
                ('cellphone', models.CharField(max_length=200, blank=True)),
                ('address', models.TextField(max_length=300, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('photo', models.ImageField(upload_to=b'', blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=b'False')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ldap_settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ldap_user', models.CharField(max_length=200)),
                ('ldap_password', models.CharField(max_length=200)),
                ('ldap_server', models.CharField(unique=True, max_length=200)),
                ('ldap_base', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=b'False')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
