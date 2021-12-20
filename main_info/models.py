from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.safestring import mark_safe

from users.models import User


class NotificationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def all(self, recipient):
        return self.get_queryset().filter(
            recipient=recipient,
            read=False
        )

    def make_all_read(self, recipient):
        """Прочитать все"""
        qs = self.get_queryset().filter(recipient=recipient, read=False)
        qs.update(read=True)

    def make_read(self, pk):
        """Ставим отметку что уведомление прочитано"""
        qs = self.get_queryset().get(id_member=pk)
        qs.read = True
        qs.save()

    def added_guild_member(self, pk):
        """Добавляем игрока к членам гильдии"""
        member = User.objects.get(id=pk)
        member.guild_member = True
        member.save()
        self.make_read(pk)

    def del_guild_member(self, pk):
        self.make_read(pk)


class Notification(models.Model):
    """Уведомление"""

    recipient = models.ForeignKey(User, verbose_name='Получатель', on_delete=models.CASCADE)
    text = models.TextField()
    display_name = models.CharField(verbose_name='Ник игрока', max_length=100, default='')
    read = models.BooleanField(default=False)
    id_member = models.IntegerField(verbose_name='Id игрока')
    objects = NotificationManager()

    def __str__(self):
        return f"Уведомление для {self.recipient.game_nick}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


def send_notifications(instance, **kwargs):
    if not instance.guild_member and instance.is_first_login:
        users_staff = User.objects.filter(staff=True)
        if users_staff.count():
            for i in users_staff:
                Notification.objects.create(
                    recipient=i,
                    display_name=instance.game_nick,
                    text=mark_safe(f'{instance.game_nick} успешно зарегистрирован!<br>Добавить его?'),
                    id_member=int(instance.id)
                )
            obj = User.objects.get(id=instance.id)
            User.objects.filter(is_first_login=True).update(is_first_login=False)
            obj.refresh_from_db()


post_save.connect(send_notifications, sender=User)
