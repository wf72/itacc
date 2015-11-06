# coding=utf-8
import ldap
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from addressbook.models import Contact
from addressbook.models import Settings


def settings(item):
    """
    Получение настроек
    :param item: ключ настроек
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
    Список всех контактов
    :param request:
    :return:

    """
    user = request.user
    if request.POST:
        search_string = request.POST.get('search_string')
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
    return redirect('addressbook:index')


@user_passes_test(user_can_edit, login_url="/login/")
def add(request):
    """
    Добавление нового контакта

    :param request:
    :return:

    """
    return render(request, 'addressbook/edit.html')


@user_passes_test(user_can_edit, login_url="/login/")
@require_POST
def editpost(request):
    """
    Отправляет изменения контакта в базу

    :param request:
    :return:

    """
    contact_id = request.POST.get('id')
    if contact_id != "add_contact":
        selected_contact = get_object_or_404(Contact, pk=contact_id)
    else:
        selected_contact = Contact()
        selected_contact.pk = None

    selected_contact.lastname = request.POST.get('lastname')
    selected_contact.firstname = request.POST.get('firstname')
    selected_contact.fathername = request.POST.get('fathername')
    selected_contact.company = request.POST.get('company')
    selected_contact.position = request.POST.get('position')
    selected_contact.department = request.POST.get('department')
    selected_contact.phone = request.POST.get('phone')
    selected_contact.cellphone = request.POST.get('cellphone')
    selected_contact.address = request.POST.get('address')
    selected_contact.email = request.POST.get('email')
    if request.POST.get('birthday'):
        date_object = datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d')
        selected_contact.birthday = date_object
    if request.POST.get('active'):
        selected_contact.active = True
    else:
        selected_contact.active = False
    selected_contact.save()
    return redirect('addressbook:index')
#

@user_passes_test(user_can_edit, login_url="/login/")
def ldap_sync(request):
    """Синхронизация с Active Directory"""
    l = ldap.initialize(settings("ldap_server"))
    try:
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind_s(settings('ldap_user'), settings('ldap_password'))
        base = settings('ldap_base')
        criteria = "(&(mail=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(objectClass=user))"
        attributes = {'sn': 'lastname', 'givenName': 'firstname', 'mail': 'email',
                      'telephoneNumber': 'phone', 'mobile': 'cellphone',
                      'l': 'address', 'streetAddress': 'address', 'department': 'department',
                      'company': 'company', 'displayName': None, 'sAMAccountName': 'login', 'title': 'position'}
        result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes.keys())
        results = [entry for dn, entry in result if isinstance(entry, dict)]

        for contact in results:
            contact_data = {}
            contact_login = ''
 
            for key in contact.keys():
                if key in ('l', 'streetAddress'):
                    contact_data['address'] = ", ".join([contact_data.get('address', ''), contact[key][0]])
                elif key == 'sAMAccountName':
                    contact_login = contact[key][0]
                elif key == 'displayName':
                    splitted_name = contact[key][0].split()
                    if len(splitted_name) == 3:
                        contact_data['lastname'], contact_data['firstname'], contact_data['fathername'] = splitted_name
                    elif len(splitted_name) == 2:
                        contact_data['lastname'], contact_data['firstname'] = splitted_name
                    elif len(splitted_name) == 1:
                        contact_data['lastname'] = contact[key][0]
                else:
                    contact_data[attributes[key]] = contact[key][0]

            try:
                new_contact, created = Contact.objects.update_or_create(login=contact_login, defaults=contact_data)
            except Exception:
                new_contact = ""
    finally:
        l.unbind()
    return redirect('addressbook:index')
