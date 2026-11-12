from django.db import models

class CurrencyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, blank=True)

    category = models.ForeignKey(
        CurrencyCategory,
        on_delete=models.PROTECT,
        related_name='currencies'
    )

    def __str__(self):
        return f'{self.code} - {self.name}'


class RateSource(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='exchange_rates'
    )

    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='base_exchange_rates'
    )

    source = models.ForeignKey(
        RateSource,
        on_delete=models.PROTECT,
        related_name='exchange_rates'
    )

    rate = models.DecimalField(max_digits=18, decimal_places=6)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['currency', 'base_currency', 'source', 'date'],
                name='unique_daily_exchange_rate'
            )
        ]

    def __str__(self):
        return f'{self.currency.code}/{self.base_currency.code}: {self.rate}'

class ImportLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('error', 'Ошибка')
    ]

    source = models.ForeignKey(
        RateSource,
        on_delete=models.PROTECT,
        related_name='import_logs'
    )

    import_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f'{self.source.name} - {self.status}'