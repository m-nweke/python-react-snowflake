# Generated by Django 5.2.1 on 2025-05-24 01:14

from django.db import migrations
from decimal import Decimal
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password


def load_mock_data(apps, schema_editor):
    Stock = apps.get_model('api', 'Stock')
    Portfolio = apps.get_model('api', 'Portfolio')
    PortfolioStock = apps.get_model('api', 'PortfolioStock')
    Transaction = apps.get_model('api', 'Transaction')
    StockPrice = apps.get_model('api', 'StockPrice')
    User = apps.get_model('auth', 'User')

    user = User.objects.create(
        username='testuser',
        email='test@example.com',
        password=make_password('testpass123')
    )

    stocks = [
        Stock.objects.create(symbol='AAPL', company_name='Apple Inc.', sector='Technology', industry='Consumer Electronics'),
        Stock.objects.create(symbol='MSFT', company_name='Microsoft Corporation', sector='Technology', industry='Software'),
        Stock.objects.create(symbol='GOOGL', company_name='Alphabet Inc.', sector='Technology', industry='Internet Services'),
    ]

    portfolio = Portfolio.objects.create(
        name='Tech Portfolio',
        description='Technology focused portfolio',
        user=user
    )

    today = datetime.now().date()
    for stock in stocks:
        base_price = Decimal('150.00') if stock.symbol == 'AAPL' else Decimal('300.00') if stock.symbol == 'MSFT' else Decimal('2800.00')
        for i in range(30):
            date = today - timedelta(days=i)
            price = base_price + Decimal(str(i * 0.5))
            StockPrice.objects.create(
                stock=stock,
                date=date,
                open_price=price,
                high_price=price,
                low_price=price,
                close_price=price,
                volume=1000000
            )

    for stock in stocks:
        shares = 10 if stock.symbol == 'AAPL' else 5 if stock.symbol == 'MSFT' else 2
        latest_price = StockPrice.objects.filter(stock=stock).latest('date').close_price

        PortfolioStock.objects.create(
            portfolio=portfolio,
            stock=stock,
            shares=shares,
            average_price=latest_price
        )

        Transaction.objects.create(
            portfolio=portfolio,
            stock=stock,
            transaction_type='BUY',
            shares=shares,
            price_per_share=latest_price,
            transaction_date=today - timedelta(days=1),
        )


def remove_mock_data(apps, schema_editor):
    Stock = apps.get_model('api', 'Stock')
    Portfolio = apps.get_model('api', 'Portfolio')
    User = apps.get_model('auth', 'User')

    Stock.objects.all().delete()
    Portfolio.objects.all().delete()
    User.objects.filter(username='testuser').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_mock_data, remove_mock_data),
    ]
