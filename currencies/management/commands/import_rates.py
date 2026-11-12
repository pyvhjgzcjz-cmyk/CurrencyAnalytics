from datetime import timedelta, datetime
from decimal import Decimal, ROUND_HALF_UP
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from xml.etree import ElementTree as ET

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from currencies.models import (
    Currency,
    RateSource,
    ExchangeRate,
    ImportLog
)


class Command(BaseCommand):
    help = 'Загрузка курсов валют с сайта ЦБ РФ'

    def handle(self, *args, **options):
        source = RateSource.objects.filter(
            is_active=True,
            api_url__icontains='cbr.ru/scripts/XML_daily.asp'
        ).first()

        if not source:
            raise CommandError('Источник ЦБ РФ не найден или отключён.')

        rub = Currency.objects.filter(code='RUB').first()

        if not rub:
            raise CommandError('В базе отсутствует валюта RUB.')

        currencies = {
            currency.code: currency
            for currency in Currency.objects.all()
        }

        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=29)

        created_count = 0
        updated_count = 0

        try:
            current_date = start_date

            while current_date <= end_date:
                params = urlencode({
                    'date_req': current_date.strftime('%d/%m/%Y')
                })

                url = f'{source.api_url}?{params}'

                request = Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )

                with urlopen(request, timeout=15) as response:
                    xml_data = response.read()

                root = ET.fromstring(xml_data)

                actual_date = datetime.strptime(
                    root.attrib['Date'],
                    '%d.%m.%Y'
                ).date()

                for item in root.findall('Valute'):
                    code = item.findtext('CharCode')

                    if code not in currencies:
                        continue

                    nominal = Decimal(
                        item.findtext('Nominal').replace(',', '.')
                    )

                    value = Decimal(
                        item.findtext('Value').replace(',', '.')
                    )

                    rate = (value / nominal).quantize(
                        Decimal('0.000001'),
                        rounding=ROUND_HALF_UP
                    )

                    obj, created = ExchangeRate.objects.update_or_create(
                        currency=currencies[code],
                        base_currency=rub,
                        source=source,
                        date=actual_date,
                        defaults={'rate': rate}
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                current_date += timedelta(days=1)

            ImportLog.objects.create(
                source=source,
                status='success'
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Импорт завершён! '
                    f'Новых записей: {created_count}. '
                    f'Обновлено: {updated_count}.'
                )
            )

        except Exception as error:
            ImportLog.objects.create(
                source=source,
                status='error',
                error_message=str(error)
            )

            raise CommandError(f'Ошибка импорта: {error}')