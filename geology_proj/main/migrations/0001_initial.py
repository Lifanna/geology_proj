# Generated by Django 3.2.18 on 2023-03-22 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Логин пользователя')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(default='нет', max_length=50, verbose_name='Отчество')),
                ('phone_number', models.CharField(default='Не указано', max_length=50, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('name', models.TextField(verbose_name='Полное наименование')),
                ('used_enginery', models.TextField(verbose_name='Используемая техника')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('geologist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='geologist_id', to=settings.AUTH_USER_MODEL, verbose_name='Геолог')),
                ('mbu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mbu_id', to=settings.AUTH_USER_MODEL, verbose_name='МБУ')),
                ('pmbou', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pmbou_id', to=settings.AUTH_USER_MODEL, verbose_name='ПМБОУ')),
            ],
            options={
                'verbose_name': 'Лицензия',
                'verbose_name_plural': 'Лицензии',
            },
        ),
        migrations.CreateModel(
            name='LicenseStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Статус лицензии',
                'verbose_name_plural': 'Статусы лицензий',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Линия',
                'verbose_name_plural': 'Линии',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Наименование роли')),
            ],
            options={
                'verbose_name': 'Роль (Должность)',
                'verbose_name_plural': 'Роли (Должности)',
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Статус задания',
                'verbose_name_plural': 'Статусы заданий',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование бригады')),
            ],
            options={
                'verbose_name': 'Бригада',
                'verbose_name_plural': 'Бригады',
            },
        ),
        migrations.CreateModel(
            name='WaterCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Водоток',
                'verbose_name_plural': 'Водотоки',
            },
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Скважина',
                'verbose_name_plural': 'Скважины',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=255, verbose_name='Брифинг')),
                ('description', models.TextField(verbose_name='Текст задания')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.license', verbose_name='Лицензия')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.line', verbose_name='Линия')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.taskstatus', verbose_name='Статус')),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.well', verbose_name='Скважина')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.AddField(
            model_name='license',
            name='primary_watercourse',
            field=models.ManyToManyField(related_name='primary_wc_id', to='main.WaterCourse', verbose_name='Главный водоток'),
        ),
        migrations.AddField(
            model_name='license',
            name='secondary_watercourse',
            field=models.ManyToManyField(related_name='secondary_wc_id', to='main.WaterCourse', verbose_name='Побочный водоток'),
        ),
        migrations.AddField(
            model_name='license',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.licensestatus', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.role', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.team', verbose_name='Номер бригады'),
        ),
    ]
