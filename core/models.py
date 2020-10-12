from curses.ascii import isdigit

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from core.validators import account_number_validator, isdigit_validator
from django.conf import settings
from django.contrib.auth.models import AbstractUser as BaseUser, UserManager, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=150)
    uid = models.CharField(max_length=250, unique=True)
    email = models.EmailField(blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'uid'
    objects = UserManager()

    def __str__(self):
        return self.phone or self.email or self.uid

    class Meta:
        db_table = 'auth_user'


class Company(models.Model):
    company_name = models.TextField(max_length=1000, verbose_name='Полное название')
    company_short_name = models.TextField(max_length=1000, verbose_name='Сокращенное название')

    inn = models.CharField(primary_key=True, max_length=50, validators=[isdigit_validator], verbose_name='ИНН')
    ogrn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ОГРН')
    revenue_2019 = models.CharField(max_length=250, verbose_name='Доход за 2019')
    revenue_2018 = models.CharField(max_length=250, verbose_name='Доход за 2018')
    revenue_growth = models.CharField(max_length=250, verbose_name='Рост выручки')
    revenue_growth_perc = models.CharField(max_length=250, verbose_name='Рост выручки в процентах')
    purchases_wins = models.PositiveIntegerField(verbose_name='Удачных покупок')
    purchases_total = models.PositiveIntegerField(verbose_name='Всего покупок')
    purchases_lost = models.PositiveIntegerField(verbose_name='Покупок потеряно')
    revenue_lost = models.CharField(max_length=250, verbose_name='Потерянный доход')
    bg_overpayment_perc = models.CharField(max_length=250, verbose_name='Перепата в процентах')
    bg_sum = models.CharField(max_length=250, verbose_name='Сумма')

    was_processed_manually = models.BooleanField(default=False, verbose_name='Документы проверены')

    competitor_inn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ИНН Конкурента')
    competitor_ogrn = models.CharField(max_length=50, validators=[isdigit_validator], verbose_name='ОГРН Конкурента')
    competitor_full_name = models.TextField(max_length=1000, verbose_name='Полное название конкурента')
    competitor_short_name = models.TextField(max_length=1000, verbose_name='Сокращенное название конкурента')
    competitor_growth_percent = models.CharField(max_length=250, verbose_name='Рост выручки конкурента в процентах')
    competitor_purchases_wins = models.PositiveIntegerField(verbose_name='Удачных покупок конкурента')
    competitor_purchases_total = models.PositiveIntegerField(verbose_name='Всего покупок конкурента')
    competitor_bg_saving_economy = models.BigIntegerField(verbose_name='Экономия конкурента')

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='companies', blank=True, through='core.CompanyUser', verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании(лендинги)'

    def __str__(self):
        return f'{self.inn} {self.company_name}'


class CompanyUser(models.Model):
    company = models.ForeignKey(Company, related_name='company_users', on_delete=models.CASCADE, verbose_name='Компания')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company_users', on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано в')
    was_processed = models.BooleanField(default=False, verbose_name='Было обработано')

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
    company = models.ForeignKey('Company', related_name='company_recommends', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Компания')
    customer = models.TextField(max_length=1000, verbose_name='Заказчик')
    topic = models.TextField(max_length=1000, verbose_name='Описание закупки')
    probability_of_victory = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Вероятность победы')
    account_number = models.CharField(max_length=250, verbose_name='Номер тендера')
    total = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Сумма')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    federal_law = models.CharField(max_length=20, verbose_name='ФЗ')
    warranty_approved = models.BooleanField(default=False, verbose_name='Одобрена гарантия')
    warranty_sum = models.PositiveIntegerField(verbose_name='Сумма гарантии')
    tender_link = models.URLField(verbose_name='Ссылка на тендер')

    class Meta:
        verbose_name = 'Рекомендация для компании'
        verbose_name_plural = 'Рекомендации для компании'


class Warranty(models.Model):
    company = models.ForeignKey('Company', related_name='warranties', on_delete=models.CASCADE, verbose_name='Компания')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='warranties', on_delete=models.CASCADE,)
    contact_name = models.TextField(max_length=1000, blank=True, verbose_name='Имя')
    phone = models.BigIntegerField(null=True, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Почта')
    purchase_number = models.CharField(max_length=50, validators=[isdigit_validator],
                                       verbose_name='Реестровый номер торгов')
    bg_sum = models.CharField(max_length=250, verbose_name='Сумма')
    law = models.CharField(max_length=100, verbose_name='Закон')
    bg_type = models.CharField(max_length=100, verbose_name='Вид банковской гарантии')
    purchase_date = models.DateTimeField(verbose_name='Дата тендера(аукциона)')
    start_date = models.DateTimeField(verbose_name='Дата начала гарантии')
    end_date = models.DateTimeField(verbose_name='Дата конца гарантии')

    class Meta:
        verbose_name = 'Заявка на гарантию'
        verbose_name_plural = 'Заявки на гарантию'
