# Generated by Django 3.2.18 on 2023-03-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20230323_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование'),
        ),
    ]
