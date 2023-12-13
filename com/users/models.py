from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        "Пользователь",
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Имя пользователя содержит недопустимый символ",
            )
        ],
    )

    def __str__(self):
        return self.username
