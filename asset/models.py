# coding=utf-8
from django.db import models

# from addressbook.models import Contact


class Partner(models.Model):
    """
    Производитель, поставщик или любое другое юридическое лицо
    """
    Name = models.CharField()
    Address = models.CharField()
    Phone = models.CharField(max_length=200, blank=True)
    Email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.Name


class DevTypes(models.Model):
    """ Типы устройств
    """
    Name = models.CharField()
    Manufacturer = models.ForeignKey('Manufacturer')

    def __unicode__(self):
        return "%s %s" % (self.Manufacturer, self.Name)


class Dev(models.Model):
    """Устройства: компьютеры, принтеры и т.д."""
    Name = models.CharField()
    Type = models.ForeignKey(DevTypes)
    Manufacturer = models.ForeignKey('Manufacturer')
    SerialNumber = models.CharField(unique=True, blank=True)
    InventoryNumber = models.CharField(unique=True)
    WarrantyPeriod = models.DateField()
    Cost = models.IntegerField(blank=True)
    DatePurchase = models.DateField(blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.Manufacturer, self.Name, self.InventoryNumber)


class Soft(models.Model):
    """Ленцзии на программы, лицензии на пользователя, сами программы и всё что с ними связано"""
    Name = models.CharField()
    Developer = models.CharField()
    Validity = models.DateField(blank=True)

    def __unicode__(self):
        return "%s %s" % (self.Developer, self.Name)


class Supplie(models.Model):
    """ Расходники: картриджи, бумага, тонер, ЗиПы, рекмпоплекты и т.д.
    """
    Name = models.CharField()
    Type = models.ForeignKey('DevTypes')
    PartNumber = models.CharField()
    Manufacturer = models.ForeignKey('Manufacturer')

    def __unicode__(self):
        return "%s %s" % (self.Manufacturer, self.Name)


class User(models.Model):
    """ Пользователи ИТ устройств компании
    """
    Person = models.OneToOneField('Contact')
    Rights = models.ManyToManyField('UserRights')
    Department = models.ForeignKey('Department')

    def __unicode__(self):
        return self.Person


class UserRighst(models.Model):
    """ Права доступа пользователей к чему либо
    """
    Name = models.CharField()
    Value = models.CharField()

    def __unicode__(self):
        return "%s %s" % (self.Name, self.Value)


class Storage(models.Model):
    """ Место хранения
    """
    Name = models.CharField()
    Address = models.TextField(max_length=300, blank=True)
    User = models.ForeignKey('User')


class Department(models.Model):
    """ Отдел
    """
    Name = models.CharField()
    Address = models.TextField(max_length=300, blank=True)
    Responsibility = models.ForeignKey('User')


class DevMovement(models.Model):
    """
    Движения устройств
    """
    Devices = models.ManyToManyField('Department')
    StorageSender = models.ForeignKey('Storage', blank=True)
    StorageReceiver = models.ForeignKey('Storage')
    Partner = models.ForeignKey('Partner', blank=True)
    TransactionType = ['purchase', 'moving', 'utilization', 'obtaining']