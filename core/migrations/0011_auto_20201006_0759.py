# Generated by Django 3.1.1 on 2020-10-06 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_company_was_processed_manually'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyrecommend',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_recommends', to='core.company', verbose_name='Компания'),
        ),
    ]
