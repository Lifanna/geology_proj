# Generated by Django 3.2.18 on 2023-05-16 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20230513_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='watercourse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.watercourse', verbose_name='Водоток'),
        ),
    ]
