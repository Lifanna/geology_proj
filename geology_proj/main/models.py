from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class Role(models.Model):
    title = models.CharField("Наименование роли", max_length=100, unique=True)

    class Meta:
        verbose_name = "Роль (Должность)"
        verbose_name_plural = "Роли (Должности)"

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField("Наименование бригады", max_length=100, unique=True)

    class Meta:
        verbose_name = "Бригада"
        verbose_name_plural = "Бригады"

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, role, is_superuser=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if is_superuser:
            user = self.model(
                username = username,
                role=role
            )
        else:
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                username = username,
                email=self.normalize_email(email),
                role=role
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def change_password(self, user_id, password):
        user = CustomUser.objects.get(pk=user_id)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        Role.objects.get_or_create(title="администратор")
        user = self.create_user(
            username,
            "",
            password,
            role=Role.objects.get(title="администратор"),
            is_superuser=True,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField("Логин пользователя", max_length=50, unique=True)

    first_name = models.CharField("Имя", max_length=50)

    last_name = models.CharField("Фамилия", max_length=50)

    patronymic = models.CharField("Отчество", max_length=50, default="нет")

    team = models.ForeignKey(Team, verbose_name="Номер бригады", on_delete=models.CASCADE, null=True)

    phone_number = models.CharField("Номер телефона", max_length=50, default="Не указано")

    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=True, null=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Должность")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_driller(self):
        "Is the user a customer?"

        return self.role.title == "бурильщик"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class LicenseStatus(models.Model):
    name = models.CharField("Наименование", max_length=255)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус лицензии"
        verbose_name_plural = "Статусы лицензий"


class WaterCourse(models.Model):
    name = models.CharField("Наименование", max_length=255)

    parent_watercourse = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Главный водоток")

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Водоток"
        verbose_name_plural = "Водотоки"

class License(models.Model):
    short_name = models.CharField("Наименование", max_length=255)

    name = models.TextField("Полное наименование")

    geologist = models.ForeignKey(CustomUser, related_name='geologist_id', on_delete=models.SET_NULL, verbose_name="Геолог", null=True)

    status = models.ForeignKey(LicenseStatus, on_delete=models.CASCADE, verbose_name="Статус")

    used_enginery = models.TextField("Используемая техника", null=True, default="Не назначено")

    mbu = models.ForeignKey(CustomUser, related_name='mbu_id', on_delete=models.SET_NULL, verbose_name="МБУ", null=True)

    pmbou = models.ForeignKey(CustomUser, related_name='pmbou_id', on_delete=models.SET_NULL, verbose_name="ПМБОУ", null=True)

    primary_watercourse = models.ManyToManyField(WaterCourse, related_name='primary_wc_id', verbose_name="Главный водоток", blank=True)

    secondary_watercourse = models.ManyToManyField(WaterCourse, related_name='secondary_wc_id', verbose_name="Побочный водоток", blank=True)

    comment = models.TextField("Комментарий", null=True, blank=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"


class Well(models.Model):
    name = models.TextField("Наименование")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Скважина"
        verbose_name_plural = "Скважины"


class Line(models.Model):
    name = models.CharField("Наименование", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Линия"
        verbose_name_plural = "Линии"


class TaskStatus(models.Model):
    name = models.CharField("Наименование", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус задания"
        verbose_name_plural = "Статусы заданий"


class Task(models.Model):
    short_name = models.CharField("Брифинг", max_length=255)

    description = models.TextField("Текст задания")

    license = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name="Лицензия")

    line = models.ForeignKey(Line, on_delete=models.CASCADE, verbose_name="Линия")

    well = models.ForeignKey(Well, on_delete=models.CASCADE, verbose_name="Скважина")

    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Ответственный")

    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name="Статус")

    comment = models.TextField("Комментарий", null=True, blank=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
