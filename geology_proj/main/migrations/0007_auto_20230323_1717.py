# Generated by Django 3.2.18 on 2023-03-23 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_well_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='well',
        ),
        migrations.AlterField(
            model_name='license',
            name='lines',
            field=models.ManyToManyField(blank=True, through='main.LineLicenseWaterCourse', to='main.Line', verbose_name='Водотоки'),
        ),
        migrations.CreateModel(
            name='WellTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task', verbose_name='Задание')),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.well', verbose_name='Скважина')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='wells',
            field=models.ManyToManyField(through='main.WellTask', to='main.Well', verbose_name='Скважины'),
        ),
    ]