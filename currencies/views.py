from django.shortcuts import render
from django.db.models import Q

from .models import Currency, ExchangeRate, CurrencyCategory


def currency_list(request):
   
    search_query = request.GET.get('q', '').strip()

   
    selected_category = request.GET.get('category', '')

    
    currencies = Currency.objects.all().order_by('code')

   
    if search_query:
        currencies = currencies.filter(
            Q(code__icontains=search_query) |
            Q(name__icontains=search_query)
        )

    # Фильтрация по категории
    if selected_category:
        currencies = currencies.filter(
            category_id=selected_category
        )

    
    currency_data = []

    for currency in currencies:
        if currency.code == 'RUB':
            rate = None
        else:
            rate = ExchangeRate.objects.filter(
                currency=currency,
                base_currency__code='RUB'
            ).order_by('-date').first()

        currency_data.append({
            'currency': currency,
            'rate': rate
        })

    
    return render(
        request,
        'currencies/currency_list.html',
        {
            'currency_data': currency_data,
            'search_query': search_query,
            'categories': CurrencyCategory.objects.all(),
            'selected_category': selected_category
        }
    )