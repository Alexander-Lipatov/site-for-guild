from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)


class UserManager(BaseUserManager):

    def create_user(self, username=None, tel=None, game_nick=None, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not username:
            raise ValueError("Users must have an username")
        if not tel:
            raise ValueError("Users must have an telephone number")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            username=username,
            tel=tel,
            # tel=str(ZipCountry.objects.get(id=zipCode).zip_country) + tel,
            game_nick=game_nick,
        )
        # user_obj.zipCode = ZipCountry.objects.get(id=zipCode)
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin

        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, tel=None, game_nick=None, password=None):
        user = self.create_user(
            # zipCode,
            username,
            tel,
            game_nick=game_nick,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, username, tel=None, game_nick=None, password=None):

        user = self.create_user(
            # zipCode,
            username,
            tel,
            game_nick=game_nick,
            password=password,
            is_staff=True,
            is_admin=True,

        )
        return user




class User(AbstractBaseUser):
    username = models.CharField(verbose_name='Логин', max_length=30, unique=True)
    tel = models.CharField(verbose_name='Телефон', max_length=20, unique=True)
    game_nick = models.CharField(verbose_name='Ник', max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name='Активный', default=False)  # can login
    guild_member = models.BooleanField(verbose_name='Член гильдии', default=False)
    staff = models.BooleanField(verbose_name='Ранг 4', default=False)  # staff user non superuser
    admin = models.BooleanField(verbose_name='Администратор', default=False)  # superuser
    whatsapp_boolean = models.BooleanField(verbose_name='WhatsApp', null=True)  # superuser
    telegram_boolean = models.BooleanField(verbose_name='Telegram', null=True)  # superuser
    telegram_name = models.CharField(verbose_name='Имя в телеграм', max_length=100, null=True)
    viber_boolean = models.BooleanField(verbose_name='Viber', null=True)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(verbose_name="Аватар", null=True, blank=True, upload_to='avatars/images/',
                               height_field=None, width_field=None, max_length=100)
    is_first_login = models.BooleanField(default=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'username'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['tel', 'game_nick']  # ['game_nick'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.game_nick

    def get_game_nick(self):
        if self.game_nick:
            return self.game_nick
        return self.tel

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # @property
    # def is_active(self):
    #     return self.active


class Country(models.Model):
    title = models.CharField(verbose_name='Страна', max_length=20)
    tel_code = models.CharField(verbose_name='Код страны', max_length=5)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
