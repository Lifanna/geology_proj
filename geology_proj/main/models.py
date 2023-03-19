from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class Role(models.Model):
    title = models.CharField("Наименование роли", max_length=100, unique=True)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, role):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        Role.objects.get_or_create(title="администратор")
        user = self.create_user(
            email,
            password,
            role=Role.objects.get(title="администратор"),
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    first_name = models.CharField("Имя", max_length=50)

    last_name = models.CharField("Фамилия", max_length=50)

    phone_number = models.CharField("Номер телефона", max_length=50, default="Не указано")

    address = models.TextField("Адрес", default="Не указано")

    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)

    date_of_birth = models.DateField("Дата рождения", null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = CustomUserManager()

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

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
    def is_customer(self):
        "Is the user a customer?"

        return self.role.title == "потребитель"

    @property
    def is_seller(self):
        "Is the user a seller?"

        return self.role.title == "продавец"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Well(models.Model):
    pass

    class Meta:
        verbose_name = "Скважина"
        verbose_name_plural = "Скважины"
