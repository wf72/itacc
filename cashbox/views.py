# coding=utf-8
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.decorators.http import require_POST

from cashbox.models import User, CashBox


def user_can_edit(user):
    """
    Проверка на возможность редактирования
    :param user:
    :return:

    """
    return user.is_authenticated() and user.has_perm("cashbox.CashBoxSetting")


@user_passes_test(user_can_edit, login_url="/login/")
def index(request):
    """

    :param request:
    :return:
    """
    cashbox_list = CashBox.objects.order_by('name').exclude(disabled = 1)
    context = {'cashbox_list': cashbox_list}
    return render(request, 'index.html', context)

@user_passes_test(user_can_edit, login_url="/login/")
@require_POST
def rendersettings(request):
    cashbox_id = request.POST.get('id')
    cb = get_object_or_404(CashBox, pk=cashbox_id)
    file_base_path = cb.file_base_path if cb.file_base_path else 'base.txt'
    # file_flag_path = cb.file_flag_path if cb.file_flag_path else 'flag.txt'    # как передать два фала в одном ответе?
    textfile_header = '''##@@&&
#
'''
    textfile1 = ''
    textfile2 = ''
    textfile_bottom = '$$$ADD'

    if request.POST.get('users'):
        textfile_bottom = '$$$CLR{NO_TOV}{USR}{NAB_P}'
        users = User.objects.filter(cashbox=cb).exclude(disabled = 1)
        cashbox_permissions = set([ user.cashbox_permission for user in users ])
        for item in cashbox_permissions:
            textfile1 += item.totext()
        for user in users:
            textfile1 += user.usertotext()
    if request.POST.get('settings'):
        textfile2 += cb.settings.totext()

    if textfile1 or textfile2:
        result = unicode(textfile_header)
        if textfile1:
            result += unicode(textfile1)
        if textfile2:
            result += unicode(textfile2)
        result += unicode(textfile_bottom)

    if len(result.splitlines()) > 2:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_base_path
        response.write(result)
        return response
    else:
        return redirect('cashbox:index')


@user_passes_test(user_can_edit, login_url="/login/")
def cashbox_users(request, cashbox_id):
    cb = get_object_or_404(CashBox, pk=cashbox_id)
    users = User.objects.filter(cashbox=cb).exclude(disabled = 1).exclude(name = 'Администратор')
    context = {'users': users}
    return render(request, 'cashbox_users.html', context)