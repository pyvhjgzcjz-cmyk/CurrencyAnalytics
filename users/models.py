from django.db import models
from django.db import models
from django.contrib.auth.models import User
from currencies.models import Currency

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'Пользователь'),
            ('admin', 'Администратор')
        ],
        default='user'
    )

    def __str__(self):
        return self.user.username

class FavoriteCurrency(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_currencies'
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='favorite_by'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'currency'],
                name='unique_user_favorite_currency'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.currency.code}'


class RateAlert(models.Model):
    CONDITION_CHOICES = [
        ('above', 'Выше заданного курсе'),
        ('below', 'Ниже заданного курса')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rate_alerts'
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    target_rate = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )

    is_active = models.BooleanField(default=True)

    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.currency.code}'


class UserActivity(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    action = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.action}'