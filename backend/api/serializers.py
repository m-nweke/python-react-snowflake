from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Portfolio, Stock, PortfolioStock, Transaction, StockPrice

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class PortfolioStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioStock
        fields = ('id', 'stock', 'shares', 'average_price', 'current_value', 'last_updated')

    def get_current_value(self, obj):
        try:
            latest_price = obj.stock.prices.latest('date').close_price
            return float(obj.shares) * float(latest_price)
        except StockPrice.DoesNotExist:
            return None

class TransactionSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'portfolio', 'stock', 'transaction_type', 'shares', 
                 'price_per_share', 'transaction_date', 'notes', 'created_at')

class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    stocks = PortfolioStockSerializer(many=True, read_only=True)
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'name', 'description', 'stocks', 
                 'total_value', 'created_at', 'updated_at')

    def get_total_value(self, obj):
        total = 0
        for stock in obj.stocks.all():
            if stock.current_value:
                total += stock.current_value
        return total

class StockPriceSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = StockPrice
        fields = ('id', 'stock', 'date', 'open_price', 'high_price', 
                 'low_price', 'close_price', 'volume', 'created_at') 