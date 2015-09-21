# coding=utf-8
from django.db import models

# from addressbook.models import Contact


class Partner(models.Model):
    """ Производитель, поставщик или любое другое юридическое лицо """
    name = models.CharField()
    address = models.CharField()
    phone = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.name


class DevTypes(models.Model):
    """ Типы устройств """
    name = models.CharField()
    manufacturer = models.ForeignKey('Manufacturer')

    def __unicode__(self):
        return "%s %s" % (self.manufacturer, self.name)


class Dev(models.Model):
    """ Устройство: компьютеры, принтеры и т.д. """
    name = models.CharField()
    type = models.ForeignKey(DevTypes)
    manufacturer = models.ForeignKey('Manufacturer')
    serial_number = models.CharField(unique=True, blank=True)
    inventory_number = models.CharField(unique=True)
    warranty_period = models.DateField()
    cost = models.IntegerField(blank=True)
    date_purchase = models.DateField(blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.manufacturer, self.name, self.inventory_number)


class Soft(models.Model):
    """ Лицензии на программы, лицензии на пользователя, сами программы и всё, что с ними связано """
    name = models.CharField()
    developer = models.CharField()
    validity = models.DateField(blank=True)

    def __unicode__(self):
        return "%s %s" % (self.developer, self.name)


class Supply(models.Model):
    """ Расходник: картриджи, бумага, тонер, ЗиПы, ремкомплекты и т.д. """
    name = models.CharField()
    type = models.ForeignKey('DevTypes')
    part_number = models.CharField()
    manufacturer = models.ForeignKey('Manufacturer')

    def __unicode__(self):
        return "%s %s" % (self.Manufacturer, self.Name)


class User(models.Model):
    """ Пользователь ИТ устройств компании """
    person = models.OneToOneField('Contact')
    rights = models.ManyToManyField('UserRights')
    department = models.ForeignKey('Department')

    def __unicode__(self):
        return self.Person


class UserRights(models.Model):
    """ Права доступа пользователей к чему-либо """
    name = models.CharField()
    value = models.CharField()

    def __unicode__(self):
        return "%s %s" % (self.Name, self.Value)


class Storage(models.Model):
    """ Место хранения """
    name = models.CharField()
    address = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey('User')


class Department(models.Model):
    """ Отдел """
    name = models.CharField()
    address = models.TextField(max_length=300, blank=True)
    responsibility = models.ForeignKey('User')


class DevMovement(models.Model):
    """
    Движение устройств
    """
    devices = models.ManyToManyField('Department')
    storage_sender = models.ForeignKey('Storage', blank=True)
    storage_receiver = models.ForeignKey('Storage')
    partner = models.ForeignKey('Partner', blank=True)
    transaction_type = ['purchase', 'moving', 'utilization', 'obtaining']