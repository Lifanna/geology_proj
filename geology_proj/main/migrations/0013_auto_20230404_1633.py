# Generated by Django 3.2.18 on 2023-04-04 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20230329_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='x',
            field=models.FloatField(blank=True, null=True, verbose_name='x'),
        ),
        migrations.AddField(
            model_name='well',
            name='y',
            field=models.FloatField(blank=True, null=True, verbose_name='y'),
        ),
        migrations.AddField(
            model_name='well',
            name='z',
            field=models.FloatField(blank=True, null=True, verbose_name='z'),
        ),
    ]