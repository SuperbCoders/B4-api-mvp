# Generated by Django 3.1.1 on 2020-09-21 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_warranty_bg_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warranty',
            name='contact_name',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='warranty',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='warranty',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Телефон'),
        ),
    ]