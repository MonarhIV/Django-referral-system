from django.contrib.auth.models import AbstractUser
from django.db import models
import string
import random


def generate_invite_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code, verbose_name='Инвайт-код')
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='Активированный чужой инвайт-код')
    # invited_users: обратная связь через related_name

    def __str__(self):
        return self.phone or self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
