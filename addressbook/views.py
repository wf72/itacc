# coding=utf-8
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from addressbook.models import Contact
from addressbook.models import Ldap_settings
from django.db.models import Q
from datetime import datetime
import ldap

def ldap_settings(item):
    """
    Получение настроек ldap
    :param item:
    :return:
    """
    settings = Ldap_settings.objects.get(active=True)
    if settings:
        if item == 'ldap_user':
            return settings.ldap_user
        elif item == 'ldap_password':
            return settings.ldap_password
        elif item == 'ldap_base':
            return settings.ldap_base
        elif item == 'ldap_server':
            return settings.ldap_server

def user_can_edit(user):
    """
    Проверка на возможность редактирования
    :param user:
    :return:
    """
    return user.is_authenticated() and user.has_perm("addressbook.Contact")

def search_contact(search_string):
    """
    Поиск контактов, почему-то ищет только с учетом регистра, нужно исправить
    :param search_string:
    :return:
    """
    #search_string=search_string.lower()
    return Contact.objects.filter(Q(lastname__icontains=search_string) | Q(firstname__icontains=search_string) | Q(fathername__icontains=search_string) )


def index(request):
    """
    Список контактов
    :param request:
    :return:
    """
    user = request.user
    if request.POST:
        search_string=request.POST['search_string']
    else:
        search_string = ""
    if search_string == "":
        contacts_list = Contact.objects.order_by('lastname')
    else:
        contacts_list=search_contact(search_string).order_by('lastname')

    context = {'contacts_list': contacts_list,'can_edit': user_can_edit(user),'search_string': search_string, 'current_day':datetime.now()}
    return render(request,'addressbook/index.html',context)

def detail(request,contact_id):
    """
    Просмотр контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request,'addressbook/detail.html',{'contact':contact})

@user_passes_test(user_can_edit, login_url="/login/")
def edit(request,contact_id):
    """
    Открытие формы редактирования контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request,'addressbook/edit.html',{'contact':contact})

@user_passes_test(user_can_edit, login_url="/login/")
def delete(request,contact_id):
    """
    Удаление контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return HttpResponseRedirect(reverse('addressbook:index' ))

@user_passes_test(user_can_edit, login_url="/login/")
def add(request):
    """
    Добавление нового контакта
    :param request:
    :return:
    """
    return render(request,'addressbook/edit.html')

@user_passes_test(user_can_edit, login_url="/login/")
def editpost(request):
    """ Отправляет изменения контакта в базу
    :param request:
    :return:
    """
    contact_id=request.POST['id']
    if contact_id <> "add_contact":
        selected_contact = get_object_or_404(Contact, pk=contact_id)
    else:
        selected_contact = Contact()
        selected_contact.pk=None

    selected_contact.lastname = request.POST['lastname']
    selected_contact.firstname = request.POST['firstname']
    selected_contact.fathername = request.POST['fathername']
    selected_contact.company = request.POST['company']
    selected_contact.position = request.POST['position']
    selected_contact.department = request.POST['department']
    selected_contact.phone = request.POST['phone']
    selected_contact.cellphone = request.POST['cellphone']
    selected_contact.address = request.POST['address']
    selected_contact.email = request.POST['email']
    #selected_contact.photo = request.POST['lastname']
    if request.POST['birthday']:
        date_object = datetime.strptime(request.POST['birthday'], '%Y-%m-%d')
        selected_contact.birthday = date_object
    try:
        if request.POST['active'] == 'active':
            selected_contact.active = 1
    except:
        selected_contact.active = 0
    selected_contact.save()
    return HttpResponseRedirect(reverse('addressbook:index' ))

@user_passes_test(user_can_edit, login_url="/login/")
def ldap_sync(request):
    """Синхронизация с Active Directory"""
    l = ldap.initialize("ldap://192.168.1.5")
    try:
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_REFERRALS, 0)
        bind = l.simple_bind_s(ldap_settings('ldap_user'), ldap_settings('ldap_password'))
        base = ldap_settings('ldap_base')
        #criteria = "(&(objectClass=user)(sAMAccountName=username))"
        criteria = "(&(mail=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(objectClass=user))"
        attributes = ['sn','givenName', 'mail','telephoneNumber', 'mobile', 'l', 'streetAddress','department','company','displayName','sAMAccountName',]
        result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
        results = [entry for dn, entry in result if isinstance(entry, dict)]
        for contact in results:
            Llastname=''
            Llastname2=''
            Lfirstname=''
            Lfirstname2=''
            Lfathername=''
            Lcompany=''
            Lposition=''
            Ldepartment=''
            Lphone=''
            Lcellphone=''
            Laddress=''
            Lemail=''
            Llogin=''
            for key in contact.keys():
                if key=='sn':
                    Llastname2 = contact[key][0]
                elif key == 'givenName':
                    Lfirstname2 = contact[key][0]
                elif key == 'mail':
                    Lemail = contact[key][0]
                elif key == 'telephoneNumber':
                    Lphone = contact[key][0]
                elif key == 'mobile':
                    Lcellphone = contact[key][0]
                elif key == 'l':
                    Laddress = contact[key][0]
                elif key == 'streetAddress':
                    Laddress =  Laddress + ", " + contact[key][0]
                elif key == 'department':
                    Ldepartment = contact[key][0]
                elif key == 'company':
                    Lcompany = contact[key][0]
                elif key == 'sAMAccountName':
                    Llogin = contact[key][0]
                elif key == 'displayName':
                    if len(contact[key][0].split()) == 3:
                        Llastname,Lfirstname,Lfathername = contact[key][0].split()
                    elif len(contact[key][0].split()) == 2:
                        Llastname,Lfirstname = contact[key][0].split()
                    elif len(contact[key][0].split()) == 1:
                        Llastname = contact[key][0]

                Llastname = Llastname if Llastname else Llastname2
                Lfirstname = Lfirstname if Lfirstname else Lfirstname2
            try:
                new_contact = Contact.objects.get(login=Llogin)
            except:
                new_contact=""
            if not new_contact:
                new_contact = Contact.objects.create(login=Llogin,lastname=Llastname,firstname=Lfirstname,fathername=Lfathername,company=Lcompany,position=Lposition,department=Ldepartment,phone=Lphone,cellphone=Lcellphone,address=Laddress,email=Lemail,active=True)
                new_contact.save()
            else:
                changed=False
                if new_contact.lastname<>Llastname:
                    new_contact.lastname=Llastname
                    changed=True
                if new_contact.firstname<>Lfirstname:
                    new_contact.firstname=Lfirstname
                    changed=True
                if new_contact.fathername<>Lfathername:
                    new_contact.fathername=Lfathername
                    changed=True
                if new_contact.company<>Lcompany:
                    new_contact.company=Lcompany
                    changed=True
                if new_contact.position<>Lposition:
                    new_contact.position=Lposition
                    changed=True
                if new_contact.department<>Ldepartment:
                    new_contact.department=Ldepartment
                    changed=True
                if new_contact.phone<>Lphone:
                    new_contact.phone=Lphone
                    changed=True
                if new_contact.cellphone<>Lcellphone:
                    new_contact.cellphone=Lcellphone
                    changed=True
                if new_contact.address<>Laddress:
                    new_contact.address=Laddress
                    changed=True
                if new_contact.email<>Lemail:
                    new_contact.email=Lemail
                    changed=True
                if changed:
                    new_contact.save()

    finally:
        l.unbind()
    return HttpResponseRedirect(reverse('addressbook:index' ))