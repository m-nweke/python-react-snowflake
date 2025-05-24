from django.contrib import admin
from .models import Portfolio, Stock, PortfolioStock, Transaction, StockPrice

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at', 'updated_at')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'company_name', 'sector', 'industry', 'last_updated')
    search_fields = ('symbol', 'company_name', 'sector', 'industry')
    list_filter = ('sector', 'industry')

@admin.register(PortfolioStock)
class PortfolioStockAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'shares', 'average_price', 'last_updated')
    search_fields = ('portfolio__name', 'stock__symbol')
    list_filter = ('last_updated',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'transaction_type', 'shares', 
                   'price_per_share', 'transaction_date')
    search_fields = ('portfolio__name', 'stock__symbol')
    list_filter = ('transaction_type', 'transaction_date')

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock', 'date', 'open_price', 'high_price', 
                   'low_price', 'close_price', 'volume')
    search_fields = ('stock__symbol',)
    list_filter = ('date',)
