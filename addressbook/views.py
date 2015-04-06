# coding=utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from addressbook.models import Contact
from addressbook.models import Settings
from django.db.models import Q
from datetime import datetime
import ldap


def settings(item):
    """
    Получение настроек
    :param item:
    :return:
    """
    if item:
        value = Settings.objects.get(key=item).value
        if value:
            return value


def user_can_edit(user):
    """
    Проверка на возможность редактирования
    :param user:
    :return:
    """
    return user.is_authenticated() and user.has_perm("addressbook.Contact")


def search_contact(search_string):
    """
    Поиск контактов. С sqlite не работает поиск без учета регистра.
    Ссылка на документацию: https://docs.djangoproject.com/en/dev/ref/databases/#sqlite-string-matching
    :param search_string:
    :return:
    """
    return Contact.objects.filter(Q(lastname__icontains=search_string) |
                                  Q(firstname__icontains=search_string) | Q(fathername__icontains=search_string))


def index(request):
    """
    Список контактов
    :param request:
    :return:
    """
    user = request.user
    if request.POST:
        search_string = request.POST['search_string']
    else:
        search_string = ""
    if search_string == "":
        contacts_list = Contact.objects.order_by('lastname')
    else:
        contacts_list = search_contact(search_string).order_by('lastname')

    context = {'contacts_list': contacts_list, 'can_edit': user_can_edit(user),
               'search_string': search_string, 'current_day': datetime.now()}
    return render(request, 'addressbook/index.html', context)


def detail(request, contact_id):
    """
    Просмотр контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'addressbook/detail.html', {'contact': contact})


@user_passes_test(user_can_edit, login_url="/login/")
def edit(request, contact_id):
    """
    Открытие формы редактирования контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'addressbook/edit.html', {'contact': contact})


@user_passes_test(user_can_edit, login_url="/login/")
def delete(request, contact_id):
    """
    Удаление контакта
    :param request:
    :param contact_id:
    :return:
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return HttpResponseRedirect(reverse('addressbook: index'))


@user_passes_test(user_can_edit, login_url="/login/")
def add(request):
    """
    Добавление нового контакта
    :param request:
    :return:
    """
    return render(request, 'addressbook/edit.html')


@user_passes_test(user_can_edit, login_url="/login/")
def editpost(request):
    """ Отправляет изменения контакта в базу
    :param request:
    :return:
    """
    contact_id = request.POST['id']
    if contact_id != "add_contact":
        selected_contact = get_object_or_404(Contact, pk=contact_id)
    else:
        selected_contact = Contact()
        selected_contact.pk = None

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
    if request.POST['birthday']:
        date_object = datetime.strptime(request.POST['birthday'], '%Y-%m-%d')
        selected_contact.birthday = date_object
    try:
        if request.POST['active'] == 'active':
            selected_contact.active = 1
    except:
        selected_contact.active = 0
    selected_contact.save()
    return HttpResponseRedirect(reverse('addressbook: index'))


@user_passes_test(user_can_edit, login_url="/login/")
def ldap_sync():
    """Синхронизация с Active Directory"""
    l = ldap.initialize(settings("ldap_server"))
    try:
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind_s(settings('ldap_user'), settings('ldap_password'))
        base = settings('ldap_base')
        criteria = "(&(mail=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(objectClass=user))"
        attributes = ['sn', 'givenName', 'mail', 'telephoneNumber', 'mobile',
                      'l', 'streetAddress', 'department', 'company', 'displayName', 'sAMAccountName']
        result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
        results = [entry for dn, entry in result if isinstance(entry, dict)]

        for contact in results:
            llastname = ''
            llastname2 = ''
            lfirstname = ''
            lfirstname2 = ''
            lfathername = ''
            lcompany = ''
            lposition = ''
            ldepartment = ''
            lphone = ''
            lcellphone = ''
            laddress = ''
            lemail = ''
            llogin = ''

            for key in contact.keys():
                if key == 'sn':
                    llastname2 = contact[key][0]
                elif key == 'givenName':
                    lfirstname2 = contact[key][0]
                elif key == 'mail':
                    lemail = contact[key][0]
                elif key == 'telephoneNumber':
                    lphone = contact[key][0]
                elif key == 'mobile':
                    lcellphone = contact[key][0]
                elif key == 'l':
                    laddress = contact[key][0]
                elif key == 'streetAddress':
                    laddress =  laddress + ", " + contact[key][0]
                elif key == 'department':
                    ldepartment = contact[key][0]
                elif key == 'company':
                    lcompany = contact[key][0]
                elif key == 'sAMAccountName':
                    llogin = contact[key][0]
                elif key == 'displayName':
                    if len(contact[key][0].split()) == 3:
                        llastname, lfirstname, lfathername = contact[key][0].split()
                    elif len(contact[key][0].split()) == 2:
                        llastname, lfirstname = contact[key][0].split()
                    elif len(contact[key][0].split()) == 1:
                        llastname = contact[key][0]

                llastname = llastname if llastname else llastname2
                lfirstname = lfirstname if lfirstname else lfirstname2
            try:
                new_contact = Contact.objects.get(login=llogin)
            except:
                new_contact = ""
            if not new_contact:
                new_contact = Contact.objects.create(login=llogin, lastname=llastname, firstname=lfirstname,
                                                     fathername=lfathername, company=lcompany, position=lposition,
                                                     department=ldepartment, phone=lphone, cellphone=lcellphone,
                                                     address=laddress, email=lemail, active=True)
                new_contact.save()
            else:
                changed = False
                if new_contact.lastname != llastname:
                    new_contact.lastname = llastname
                    changed = True
                if new_contact.firstname != lfirstname:
                    new_contact.firstname = lfirstname
                    changed = True
                if new_contact.fathername != lfathername:
                    new_contact.fathername = lfathername
                    changed = True
                if new_contact.company != lcompany:
                    new_contact.company = lcompany
                    changed = True
                if new_contact.position != lposition:
                    new_contact.position = lposition
                    changed = True
                if new_contact.department != ldepartment:
                    new_contact.department = ldepartment
                    changed = True
                if new_contact.phone != lphone:
                    new_contact.phone = lphone
                    changed = True
                if new_contact.cellphone != lcellphone:
                    new_contact.cellphone = lcellphone
                    changed = True
                if new_contact.address != laddress:
                    new_contact.address = laddress
                    changed = True
                if new_contact.email != lemail:
                    new_contact.email = lemail
                    changed = True
                if changed:
                    new_contact.save()

    finally:
        l.unbind()
    return HttpResponseRedirect(reverse('addressbook: index'))