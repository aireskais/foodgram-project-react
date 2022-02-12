from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class FoodgramUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Логин должен содержать ТОЛЬКО:'
                        ' буквы/цифры(с учетом регистра),'
                        ' а также символы: .@+-',
            ),
        ]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        FoodgramUser, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        FoodgramUser, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='follow'
            ),
        )

    def __str__(self):
        return f'{self.username} follow for {self.following}'