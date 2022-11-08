from django.db import models

# from datetime import datetime, timedelta

# from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,)


class User(AbstractUser,):
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username
