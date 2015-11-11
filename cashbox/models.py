# coding=utf-8
from django.db import models


class Shop(models.Model):
    """ Магазин """
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    disabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __unicode__(self):
        return self.name


class CashBox(models.Model):
    """ Касса """
    name = models.CharField(max_length=30)
    shop = models.ForeignKey('Shop', blank=True)
    file_base_path = models.CharField('ИмяФайлаСправочника', max_length=255, blank=True)
    file_report_path = models.CharField('ИмяФайлаОтчета', max_length=255, blank=True)
    file_flag_path = models.CharField(max_length=255, verbose_name='ИмяФлагаЗагрузки', blank=True)
    disabled = models.BooleanField(default=False)
    settings = models.ForeignKey('CashBoxSetting')  # настройки касс в виде текста

    class Meta:
        verbose_name = "Кассу"
        verbose_name_plural = "Кассы"

    def __unicode__(self):
        return self.name


class BarcodeTemplate(models.Model):
    prefix = models.CharField(verbose_name=u'Префикс штрих-кода', max_length=2, default='20')
    a0 = 0
    a1 = 1
    a2 = 2
    a3 = 3
    a4 = 4
    a5 = 5
    a6 = 6
    a7 = 7
    a8 = 8
    a9 = 9
    a10 = 10
    a11 = 11
    barcode_format_choises = (
        (a0, u'Сначала вес, затем код'),
        (a1, u'Сначала код, затем вес'),
        (a2, u'Сначала вес, потом цена'),
        (a3, u'Сначала цена, потом вес'),
        (a4, u'Сначала код, потом цена'),
        (a5, u'Сначала цена, потом код'),
        (a6, u'Служебный'),
        (a7, u'Вес + артикул'),
        (a8, u'Артикул + вес'),
        (a9, u'Вес + штрих-код'),
        (a10, u'Штрих-код + вес'),
        (a11, u'Регистрация по штрих-коду + вес берется с весов'),
    )
    barcode_format = models.SmallIntegerField(choices=barcode_format_choises, default=a1, verbose_name=u'Выбор шаблона')
    code_length = models.SmallIntegerField(verbose_name=u'Число знаков первого поля', default=6)
    weight_ratio = models.FloatField(verbose_name=u'Коэффициент веса', default=0.001)
    price_multiplier = models.FloatField(verbose_name=u'Множитель цены', default=0)
    search_by_barcode = models.BooleanField(verbose_name=u'Поик по штрих-коду', default=False)
    complement_to_ean13 = models.BooleanField(verbose_name=u'Дополнять до 13 символов', default=False)

    class Meta:
        verbose_name = "Шаблон штрих-кода"
        verbose_name_plural = "Шаблоны штрих-кодов"

    def __unicode__(self):
        format_dict = [
            ['M', 'T'],
            ['T', 'M'],
            # ['M', 'T'], найти остальные обозначения
            ]
        format_barcode = self.barcode_format_choises[self.barcode_format][1]

        return "%(prefix)s + %(format)s" % {'prefix': self.prefix, 'format': format_barcode}

    def totext(self):
        return "(%(prefix)s;%(barcode_format)s;%(code_length)s;%(weight_ratio)s;" \
               "%(price_multiplier)s;%(search_by_barcode)s;%(complement_to_ean13)s\r\n" % {
            'prefix': self.prefix,
            'barcode_format': self.barcode_format,
            'code_length': self.code_length,
            'weight_ratio': self.weight_ratio,
            'price_multiplier': self.price_multiplier,
            'search_by_barcode': int(self.search_by_barcode),
            'complement_to_ean13': int(self.complement_to_ean13)
        }


class CashBoxSetting(models.Model):
    name = models.CharField(verbose_name=u'Имя кассы', max_length=30)
    kkm_po_umolchaniyu = models.IntegerField(u'ККМПоУмолчанию', default=1)
    sekcia_po_umolchaniyu = models.IntegerField(u'СекцияПоУмолчанию', default=1)
    zero = 0
    one = 1
    two = 2
    three = 3
    four = 4
    section_choices = (
        (zero, u'Все регистрации в одну секцию'),
        (one, u'Только при свободной цене'),
        (two, u'Если не указана секция'),
        (three, u'При каждой регистрации'),
        (four, u'По свободной цене в одну секцию'),
    )
    vibor_sekcii = models.SmallIntegerField(choices=section_choices, default=zero, verbose_name=u'ВыборСекции')
    # Вид чека
    pechatat_imya_kassira = models.BooleanField(u'ПечататьИмяКассира', default=False)
    pechatat_nomer_pozicii = models.BooleanField(u'ПечататьНумерациюПозиций', default=True)
    pechatat_otstup = models.BooleanField(u'ПечататьОтступ', default=True)
    odna_stroka_na_prodaju = models.BooleanField(u'ОднаСтрокаНаПРодажу', default=False)
    pechatat_kredit_kartu = models.BooleanField(u'ПечататьКредитнуюКарту', default=False)
    pechatat_poditog_pri_skidke_na_chek = models.BooleanField(u'ПечататьПодытогПриСкидкеНадбавкеНаЧек', default=False)
    pechatat_imya_tovara = models.BooleanField(u'ПечататьНаименованиеТовара', default=True)
    perenosit_imya_tovara = models.BooleanField(u'ПереноситьДлинныеНазванияТоваров', default=True)
    pechatat_kod_tovara = models.BooleanField(u'ПечататьКодТовара', default=True)
    pechatat_cifri_shk_tovara = models.BooleanField(u'ПечататьЦифрыШтрихКодаТовара', default=True)
    pechatat_shk_ean = models.BooleanField(u'ПечататьШтрихКодЕАН', default=True)
    pechatat_imya_skidok = models.BooleanField(u'ПечататьНазваниеСкидокНадбавок', default=True)
    pechatat_razdelitel_mezhdu_prodaj = models.BooleanField(u'ПечататьРазделительМеждуПродажами', default=True)
    # Режим 1
    razreshit_block_mesta = models.BooleanField(u'РазрешитьБлокировкуРабочегоМеста', default=False)
    razreshit_smenu_usera = models.BooleanField(u'РазрешитьСменуПользователяПриБлокировке', default=False)
    avtorizaciya_posle_cheka = models.BooleanField(u'АвторизацияПослеКаждогоЧека', default=False)
    vigruzhat_prodaji_pri_zotchete = models.BooleanField(u'ВыгружатьПродажиПриZОтчете', default=False)
    prodavat_zvuk_pri_oshibke = models.BooleanField(u'ПодаватьНаККМЗвуковойСигналПриОшибке', default=False)
    ignorirovat_tochku_v_kolichestve = models.BooleanField(u'ИгнорироватьТочкуВКоличестве', default=False)
    ignorirovat_tochku_v_summe = models.BooleanField(u'ИгнорироватьТочкуВСумме', default=False)
    sozdavat_tovari_pri_vozvrate = models.BooleanField(u'СоздаватьТоварыПриВозврате', default=False)
    # Режим 2
    zapretit_prodaji_v_0 = models.BooleanField(u'ЗапретитьПродажиПоНулевойЦене', default=False)
    zapretit_oplatu_bez_vvoda_summi = models.BooleanField(u'ЗапретитьОплатуБезВводаСуммы', default=False)
    kontrol_prodaji_drobnogo_kolichestva = models.BooleanField(u'КонтрольПродажиДробногоКоличества', default=False)
    zapretit_otricatelnie_ostatki = models.BooleanField(u'ЗапретитьОтрицательныеОстатки', default=False)
    dopolnyat_shk_do_13 = models.BooleanField(u'ДополнятьШтрихКодНулямиДо13Знаков', default=True)
    vibirat_edinicu_pri_registracii = models.BooleanField(u'ВыбиратьЕдиницуПриРегистрацииПоКоду', default=False)
    zaprashivat_kolichestvo_pri_podbore = models.BooleanField(u'ЗапрашиватьКоличествоПриПодборе', default=False)
    razdelyat_triadi = models.BooleanField(u'РазделятьТриады', default=True)
    zapretit_vvod_kolichestva = models.BooleanField(u'ЗапретитьВводКоличества', default=False)
    # Режим 3
    razreshit_prodaju_po_svobodnoy_cene = models.BooleanField(u'РазрешитьПродажуПоСвободнойЦене', default=True)
    zapretit_zakritie_nulevogo_cheka = models.BooleanField(u'ЗапретитьЗакрытиеНулевогоЧека', default=False)
    # Дополнительные
    razreshit_vid_oplata_2 = models.BooleanField(u'РазрешитьВидОплаты2', default=False)
    name_vid_oplata_2 = models.CharField(u'НазваниеВидаОплаты2', max_length=30, blank=True)
    razreshit_vid_oplata_3 = models.BooleanField(u'РазрешитьВидОплаты3', default=False)
    name_vid_oplata_3 = models.CharField(u'НазваниеВидаОплаты3', max_length=30, blank=True)
    razreshit_vid_oplata_4 = models.BooleanField(u'РазрешитьВидОплаты4', default=False)
    name_vid_oplata_4 = models.CharField(u'НазваниеВидаОплаты4', max_length=30, blank=True)
    pechatat_shk_cheka = models.BooleanField(u'ПечататьШтрихКодЧека', default=False)
    prefiks_shk_cheka = models.CharField(u'ПрефиксШтрихКодаЧека', max_length=10, blank=True)
    card_choices = (
        (zero, u'Не выбирать'),
        (one, u'Наличными'),
        (two, u'Типом оплаты 2'),
        (three, u'Типом оплаты 3'),
        (four, u'Типом оплаты 4'),
    )
    vibor_platej_karti_pri_oplate = models.SmallIntegerField(verbose_name=u'ВыборПлатежнойКартыПриОплате',
                                                             choices=card_choices, default=one)
    barcode_template = models.ManyToManyField('BarcodeTemplate',verbose_name='Весовые штрих-коды')

    class Meta:
        verbose_name = u"Настройки кассы"
        verbose_name_plural = u"Настройки касс"

    def totext(self):
        """
        возможность выгружать константы-настройки в следующем формате:
|<ИмяКонстанты>=<Значение>
где <ИмяКонстанты> - идентификатор константы-настройки, как задан в конфигураторе
(знакозависим), <Значение> - значение данной константы.
        :return:
        """
        text = ""
        for template in self.barcode_template.all():
            text += template.totext()

        for field in self._meta.fields:
            if field.name not in ['name', 'id']:
                text += "|%(name)s=%(value)s\r\n" % {'name': unicode(field.verbose_name), 'value': unicode(int(getattr(self, field.name)) if isinstance(getattr(self, field.name), bool) else getattr(self, field.name))}
        return text

    def __unicode__(self):
        return self.name


class CashboxPermission(models.Model):
    name = models.CharField(u'Название набора прав', max_length=30)
    vvod_koda_v_prodaje = models.BooleanField("Ввод кода в чеке продажи", default=False)
    schitivanie_shk_skanerom_v_prodaje = models.BooleanField("Считывание ШК сканером в чеке продажи", default=False)
    vvod_shk_vruchnuyu_v_prodaje = models.BooleanField("Ввод ШК вручную в чеке продажи", default=False)
    vizualniy_podbor_v_prodaje = models.BooleanField("Через визуальный подбор в чеке продажи", default=False)
    svobodnaya_cena_v_prodaje = models.BooleanField("По свободной цене в чеке продажи", default=False)
    storno_v_prodaje = models.BooleanField("Сторно в чеке продажи", default=False)
    redaktirovat_kolichestvo = models.BooleanField("Редактировать количество", default=False)
    redaktirovat_cenu = models.BooleanField("Редактировать цену", default=False)
    vozvrat_po_nomeru_cheka = models.BooleanField("Возврат по номеру чека", default=False)
    vvod_koda_v_vozvrate = models.BooleanField("Ввод кода в чеке возврата", default=False)
    schitivanie_shk_skanerom_v_vozvrate = models.BooleanField("Считывание ШК сканером в чеке возврата", default=False)
    vvod_shk_vruchnuyu_v_vozvrate = models.BooleanField("Ввод ШК вручную в чеке возврата", default=False)
    vizualniy_podbor_v_vozvrate = models.BooleanField("Через визуальный подбор в чеке возврата", default=False)
    svobodnaya_cena_v_vozvrate = models.BooleanField("По свободной цене в чеке возврата", default=False)
    procent_skidka_na_poziciyu = models.BooleanField("Процентная скидка на позицию", default=False)
    procent_nadbavka_na_poziciyu = models.BooleanField("Процентная надбавка на позицию", default=False)
    summovaya_skidka_na_poziciyu = models.BooleanField("Суммовая скидка на позицию", default=False)
    summovaya_nadbavka_na_poziciyu = models.BooleanField("Суммовая надбавка на позицию", default=False)
    procent_skidka_na_chek = models.BooleanField("Процентная скидка на чек", default=False)
    procent_nadbavka_na_chek = models.BooleanField("Процентная надбавка на чек", default=False)
    summovaya_skidka_na_chek = models.BooleanField("Суммовая скидка на чек", default=False)
    summovaya_nadbavka_na_chek = models.BooleanField("Суммовая надбавка на чек", default=False)
    fiksirovannie_skidki_nadbavki = models.BooleanField('Фиксированные скидки/надбавки', default=False)
    otmena_skidki = models.BooleanField("Отмена скидки", default=False)
    otmena_cheka = models.BooleanField("Отмена чека", default=False)
    oplata_vidom_2 = models.BooleanField("Оплата видом оплаты 2", default=False)
    summa_v_yashike = models.BooleanField("Получить сумму в денежном ящике", default=False)
    otchet_x = models.BooleanField("Снятие отчета без гашения", default=False)
    otchet_z = models.BooleanField("Снятие отчета с гашением", default=False)
    obmen = models.BooleanField("Обмен данными", default=False)
    vnesenie = models.BooleanField("Внесение", default=False)
    viplata = models.BooleanField("Выплата", default=False)
    nastroyka = models.BooleanField("Настройка программы", default=False)
    prosmotr_pechat_cheka = models.BooleanField("Просмотр/печать чека", default=False)
    oplata_vidom_3 = models.BooleanField("Оплата видом оплаты 3", default=False)
    otlojennie_cheki = models.BooleanField("Работа с отложенными чеками", default=False)
    rashirennie_otcheti = models.BooleanField("Печать расширенных отчетов", default=False)
    redaktirovat_sekciyu = models.BooleanField("Редактировать секцию", default=False)
    oplata_uslug = models.BooleanField("Оплата услуг", default=False)
    prosmotr_tovara = models.BooleanField("Просмотр товара", default=False)
    otkritie_yashika = models.BooleanField("Открытие денежного ящика", default=False)
    oplata_vidom_4 = models.BooleanField("Оплата видом оплаты 4", default=False)
    vvod_licenzii = models.BooleanField("Ввод лицензии", default=False)
    obnovlenie = models.BooleanField("Обновление", default=False)
    nalogoviy_inspektor = models.BooleanField("Налоговый инспектор", default=False)
    vihod_v_os = models.BooleanField("Выход в ОС", default=False)
    servisnoe_menu = models.BooleanField("Сервисное меню", default=False)
    izmenenie_dati_vremeni = models.BooleanField("Изменение даты/времени", default=False)
    skladskie_operacii = models.BooleanField("Складские операции", default=False)
    jdushiy_rezhim = models.BooleanField("Ждущий режим", default=False)
    prosmotr_sertificata = models.BooleanField("Просмотр сертификата", default=False)
    prodaja_sertificata = models.BooleanField("Продажа сертификата", default=False)
    oplata_sertificata = models.BooleanField("Оплата сертификата", default=False)
    uchet_vremeni = models.BooleanField("Учет рабочего времени", default=False)
    izmenenie_dati_vremeni2 = models.BooleanField("Изменение даты/времени2", default=False)
    skladskie_operacii2 = models.BooleanField("Складские операции2", default=False)

    class Meta:
        verbose_name = "Настройки прав на кассах"
        verbose_name_plural = "Настройки прав на кассах"

    def totext(self):
        return "~%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" \
               "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" \
               "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" \
               "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;\r\n" %\
               (self.id,
                unicode(self.name),
                '', '', '', '',
                int(self.vvod_koda_v_prodaje),
                int(self.schitivanie_shk_skanerom_v_prodaje),
                int(self.vvod_shk_vruchnuyu_v_prodaje),
                int(self.vizualniy_podbor_v_prodaje),
                int(self.svobodnaya_cena_v_prodaje),
                int(self.storno_v_prodaje),
                int(self.redaktirovat_kolichestvo),
                int(self.redaktirovat_cenu),
                '',
                int(self.vozvrat_po_nomeru_cheka),
                int(self.vvod_koda_v_vozvrate),
                int(self.schitivanie_shk_skanerom_v_vozvrate),
                int(self.vvod_shk_vruchnuyu_v_vozvrate),
                int(self.vizualniy_podbor_v_vozvrate),
                int(self.svobodnaya_cena_v_vozvrate),
                '',
                int(self.procent_skidka_na_poziciyu),
                int(self.procent_nadbavka_na_poziciyu),
                int(self.summovaya_skidka_na_poziciyu),
                int(self.summovaya_nadbavka_na_poziciyu),
                int(self.procent_skidka_na_chek),
                int(self.procent_nadbavka_na_chek),
                int(self.summovaya_skidka_na_chek),
                int(self.summovaya_nadbavka_na_chek),
                int(self.fiksirovannie_skidki_nadbavki),
                int(self.otmena_skidki),
                int(self.otmena_cheka),
                int(self.oplata_vidom_2),
                int(self.summa_v_yashike),
                int(self.otchet_x),
                int(self.otchet_z),
                int(self.obmen),
                int(self.vnesenie),
                int(self.viplata),
                int(self.nastroyka),
                int(self.prosmotr_pechat_cheka),
                int(self.oplata_vidom_3),
                int(self.otlojennie_cheki),
                int(self.rashirennie_otcheti),
                '', '', '',
                int(self.redaktirovat_sekciyu),
                '', '', '',
                int(self.oplata_uslug),
                '', '', '', '',
                int(self.prosmotr_tovara),
                '', '',
                int(self.otkritie_yashika),
                int(self.oplata_vidom_4),
                int(self.vvod_licenzii),
                int(self.obnovlenie),
                int(self.nalogoviy_inspektor),
                '',
                int(self.vihod_v_os),
                int(self.servisnoe_menu),
                '',
                int(self.izmenenie_dati_vremeni),
                int(self.skladskie_operacii),
                int(self.jdushiy_rezhim),
                int(self.prosmotr_sertificata),
                int(self.prodaja_sertificata),
                int(self.oplata_sertificata),
                int(self.uchet_vremeni),
                int(self.izmenenie_dati_vremeni2),
                int(self.skladskie_operacii2),
                )

    def fromtext(self, text):
        try:
            self.id, self.name, n, n, n, n, self.vvod_koda_v_prodaje, self.schitivanie_shk_skanerom_v_prodaje, \
            self.vvod_shk_vruchnuyu_v_prodaje, self.vizualniy_podbor_v_prodaje, self.svobodnaya_cena_v_prodaje, \
            self.storno_v_prodaje, self.redaktirovat_kolichestvo, self.redaktirovat_cenu, n, \
            self.vozvrat_po_nomeru_cheka, self.vvod_koda_v_vozvrate, self.schitivanie_shk_skanerom_v_vozvrate, \
            self.vvod_shk_vruchnuyu_v_vozvrate, self.vizualniy_podbor_v_vozvrate, self.svobodnaya_cena_v_vozvrate, n, \
            self.procent_skidka_na_poziciyu, self.procent_nadbavka_na_poziciyu, self.summovaya_skidka_na_poziciyu, \
            self.summovaya_nadbavka_na_poziciyu, self.procent_skidka_na_chek, self.procent_nadbavka_na_chek, \
            self.summovaya_skidka_na_chek, self.summovaya_nadbavka_na_chek, self.fiksirovannie_skidki_nadbavki, \
            self.otmena_skidki, self.otmena_cheka, self.oplata_vidom_2, self.summa_v_yashike, self.otchet_x, \
            self.otchet_z, self.obmen, self.vnesenie, self.viplata, self.nastroyka, self.prosmotr_pechat_cheka, \
            self.oplata_vidom_3, self.otlojennie_cheki, self.rashirennie_otcheti, n, n, n, self.redaktirovat_sekciyu, \
            n, n, n, self.oplata_uslug, n, n, n, n, self.prosmotr_tovara, n, n, self.otkritie_yashika, \
            self.oplata_vidom_4, self.vvod_licenzii, self.obnovlenie, self.nalogoviy_inspektor, n, \
            self.vihod_v_os, self.servisnoe_menu, n, self.izmenenie_dati_vremeni, self.skladskie_operacii, \
            self.jdushiy_rezhim, self.prosmotr_sertificata, self.prodaja_sertificata, self.oplata_sertificata, \
            self.uchet_vremeni, self.izmenenie_dati_vremeni2, self.skladskie_operacii2 = text[1:].split(';')
        except ValueError as e:
            print e

    def __unicode__(self):
        return self.name


class User(models.Model):
    """ Пользователи """
    name = models.CharField(max_length=30)
    zero = u'astronaut.bmp'
    one = u'pink flower.bmp'
    two = u'butterfly.bmp'
    picture_choices = (
        (zero, u'astronaut.bmp'),
        (one, u'pink flower.bmp'),
        (two, u'butterfly.bmp'),
    )
    picture = models.CharField(verbose_name=u'Картинка пользователя', choices=picture_choices, default=one)
    cashbox_permission = models.ForeignKey('CashboxPermission', verbose_name='Набор прав доступа')
    passwd = models.CharField(max_length=30, blank=True, null=True)
    cashbox = models.ManyToManyField('CashBox', blank=True)
    disabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __unicode__(self):
        return self.name

    def usertotext(self):

        return '&%(id)s;%(name)s;%(permission_id)s;%(passwd)s;%(ico)s;%(card)s\r\n' % \
               {'id': self.id,
                'name': unicode(self.name),
                'permission_id': self.cashbox_permission.id,
                'passwd': self.passwd,
                'ico': self.picture,
                'card': ''}
