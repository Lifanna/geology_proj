# Generated by Django 3.2.18 on 2023-04-20 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_line_watercourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Вид материала слоя (интервала)',
                'verbose_name_plural': 'Виды материалов слоев (интервалов)',
            },
        ),
        migrations.AddField(
            model_name='layermaterial',
            name='color',
            field=models.CharField(max_length=255, null=True, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='layermaterial',
            name='image',
            field=models.ImageField(null=True, upload_to='layer_materials_images/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='layermaterial',
            name='short_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Краткое наименование'),
        ),
        migrations.AddField(
            model_name='layermaterial',
            name='synonym',
            field=models.CharField(max_length=255, null=True, verbose_name='Синоним'),
        ),
        migrations.AddField(
            model_name='layermaterial',
            name='material_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.materialcategory', verbose_name='Вид материала'),
        ),
    ]
