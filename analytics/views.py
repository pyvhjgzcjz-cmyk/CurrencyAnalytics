

from django.shortcuts import render


from currencies.models import Currency, ExchangeRate


def currency_analytics(request):
    currencies = Currency.objects.exclude(
        code='RUB'
    ).order_by('code')

    selected_code = request.GET.get('currency', 'USD')

    selected_currency = currencies.filter(
        code=selected_code
    ).first()

    if selected_currency is None:
        selected_currency = currencies.first()

    rates = []

    if selected_currency:
        rates = list(
            ExchangeRate.objects.filter(
                currency=selected_currency,
                base_currency__code='RUB'
            ).order_by('-date')[:30].values(
                'date',
                'rate'
            )
        )

        rates.reverse()

    chart_data = {
        'labels': [str(item['date']) for item in rates],
        'values': [float(item['rate']) for item in rates]
    }

    print("ДАННЫЕ ДЛЯ ГРАФИКА:", chart_data)

    return render(
        request,
        'analytics/currency_analytics.html',
        {
            'currencies': currencies,
            'selected_currency': selected_currency,
            'chart_data': chart_data
        }
    )
