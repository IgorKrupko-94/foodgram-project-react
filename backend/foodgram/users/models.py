from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        help_text='Придумайте логин'
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        help_text='Укажите электронную почту'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Укажите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Укажите фамилию'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Укажите пароль'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Пользователь не может подписаться сам на себя'
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name=('Пользователь не может подписаться '
                      'на другого пользователя дважды')
            )
        ]
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
