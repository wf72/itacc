# coding=utf-8
from django.db import models


class Contact(models.Model):
    """ Контакты
    """
    login = models.CharField(max_length=40, unique=True)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    fathername = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    cellphone = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    active = models.BooleanField(default='False')

    def __unicode__(self):
        return "%s %s %s" % (self.lastname, self.firstname, self.fathername)


class Settings(models.Model):
    """ Настройки для синхронизации с AD.
    Должны быть значения: ldap_user, ldap_password, ldap_server, ldap_base
    """
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.key

# нужно исправить на предупреждение, при двух одинаковых настройках, ну либо изменить тип хранения настроек
#    def save(self, *args, **kwargs):
#        if self.active==True:
#
#            raise  NameError('Only one active settings')
#        else:
#           super(Ldap_settings, self).save(*args, **kwargs)