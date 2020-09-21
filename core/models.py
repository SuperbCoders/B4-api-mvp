from curses.ascii import isdigit

from django.db import models

from core.validators import account_number_validator, isdigit_validator
from django.conf import settings


class Company(models.Model):
    company_name = models.TextField(max_length=1000, verbose_name='Полное название')
    company_short_name = models.TextField(max_length=1000, verbose_name='Сокращенное название')

    inn = models.CharField(primary_key=True, max_length=50, validators=[isdigit_validator], verbose_name='ИНН')
    ogrn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ОГРН')
    revenue_2019 = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Доход за 2019')
    revenue_2018 = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Доход за 2018')
    revenue_growth = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Рост выручки')
    revenue_growth_perc = models.DecimalField(max_digits=5, decimal_places=2,
                                                 verbose_name='Рост выручки в процентах')
    purchases_wins = models.PositiveIntegerField(verbose_name='Удачных покупок')
    purchases_total = models.PositiveIntegerField(verbose_name='Всего покупок')
    purchases_lost = models.PositiveIntegerField(verbose_name='Покупок потеряно')
    revenue_lost = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Потерянный доход')
    bg_overpayment_perc = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Перепата в процентах')
    bg_sum = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Сумма')

    competitor_inn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ИНН Конкурента')
    competitor_ogrn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ОГРН Конкурента')
    competitor_full_name = models.TextField(max_length=1000, verbose_name='Полное название конкурента')
    competitor_short_name = models.TextField(max_length=1000, verbose_name='Сокращенное название конкурента')
    competitor_growth_percent = models.DecimalField(max_digits=5, decimal_places=2,
                                                    verbose_name='Рост выручки конкурента в процентах')
    competitor_purchases_wins = models.PositiveIntegerField(verbose_name='Удачных покупок конкурента')
    competitor_purchases_total = models.PositiveIntegerField(verbose_name='Всего покупок конкурента')
    competitor_bg_saving_economy = models.DecimalField(max_digits=50, decimal_places=2,
                                                       verbose_name='Экономия конкурента')

    users = models.ManyToManyField('auth.User', related_name='companies', blank=True, through='core.CompanyUser', verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании(лендинги)'


class CompanyUser(models.Model):
    company = models.ForeignKey(Company, related_name='company_users', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='company_users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Компания: пользователь'
        verbose_name_plural = 'Компании: привязанные пользователи'
        ordering = ['-created_at']


class CompanyProp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company_props', on_delete=models.CASCADE, )
    company = models.ForeignKey('Company', related_name='company_props', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=250, verbose_name='Название банка')
    account_number = models.CharField(max_length=16, validators=[account_number_validator], verbose_name='Номер счета')
    bik = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='БИК')
    dadata = models.JSONField(verbose_name='ДаДата')

    class Meta:
        verbose_name = 'Реквизиты компании'
        verbose_name_plural = 'Реквизиты компании'


class CompanyFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company_files', on_delete=models.CASCADE,)
    company = models.ForeignKey('Company', related_name='company_files', on_delete=models.CASCADE)
    file = models.ForeignKey('filestorage.APIFile', related_name='company_files', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Файл компании'
        verbose_name_plural = 'Файлы компании'


class CompanyRecommend(models.Model):
    company = models.ForeignKey('Company', related_name='company_recommends', on_delete=models.CASCADE)
    competitor_full_name = models.TextField(max_length=1000, verbose_name='Полное название конкурента')
    competitor_short_name = models.TextField(max_length=1000, verbose_name='Сокращенное название конкурента')
    competitor_growth_percent = models.DecimalField(max_digits=5, decimal_places=2,
                                                 verbose_name='Рост выручки конкурента в процентах')
    account_number = models.CharField(max_length=16, validators=[account_number_validator], verbose_name='Номер счета')
    total = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Сумма')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    federal_law = models.CharField(max_length=20, verbose_name='ФЗ')
    warranty_approved = models.BooleanField(default=False, verbose_name='Одобрена гарантия')
    warranty_sum = models.PositiveIntegerField(verbose_name='Сумма гарантии')

    class Meta:
        verbose_name = 'Рекомендация для компании'
        verbose_name_plural = 'Рекомендации для компании'


class Warranty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='warranties', on_delete=models.CASCADE,)
    contact_name = models.TextField(max_length=1000, blank=True, verbose_name='Имя')
    phone = models.BigIntegerField(null=True, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Почта')
    purchase_number = models.CharField(max_length=50, validators=[isdigit_validator],
                                       verbose_name='Реестровый номер торгов')
    bg_type = models.CharField(max_length=100, verbose_name='Вид банковской гарантии')
    purchase_date = models.DateTimeField(verbose_name='Дата тендера(аукциона)')
    start_date = models.DateTimeField(verbose_name='Дата начала гарантии')
    end_date = models.DateTimeField(verbose_name='Дата конца гарантии')

    class Meta:
        verbose_name = 'Заявка на гарантию'
        verbose_name_plural = 'Заявки на гарантию'
