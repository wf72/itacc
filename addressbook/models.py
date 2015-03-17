# coding=utf-8
from django.db import models

#Контакты
class Contact(models.Model):
    login = models.CharField(max_length=30,unique=True)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    fathername = models.CharField(max_length=200,blank=True)
    company = models.CharField(max_length=200,blank=True)
    position = models.CharField(max_length=200,blank=True)
    department = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=200,blank=True)
    cellphone = models.CharField(max_length=200,blank=True)
    address = models.TextField(max_length=300,blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(blank=True)
    birthday = models.DateField(blank=True,null=True)
    active = models.BooleanField(default='False')

    def __unicode__(self):
        return self.lastname+' '+self.firstname+' '+self.fathername

#Настройки LDAP для синхронизации с AD
class Ldap_settings(models.Model):
    ldap_user = models.CharField(max_length=200)
    ldap_password = models.CharField(max_length=200)
    ldap_server = models.CharField(max_length=200,unique=True)
    ldap_base = models.CharField(max_length=200)
    active = models.BooleanField(default='False',unique=False)

    def __unicode__(self):
        return self.ldap_server+' '+self.ldap_user

    def save(self, *args, **kwargs):
        if self.active==True:
           raise  NameError('Only one active settings') # нужно исправить не предупреждение, пока не знаю как
        else:
           super(Ldap_settings, self).save(*args, **kwargs)