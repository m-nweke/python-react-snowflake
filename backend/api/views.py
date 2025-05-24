from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Portfolio, Stock, PortfolioStock, Transaction, StockPrice
from .serializers import (
    PortfolioSerializer, StockSerializer, PortfolioStockSerializer,
    TransactionSerializer, StockPriceSerializer
)

# Create your views here.

class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        portfolio = self.get_object()
        stock_id = request.data.get('stock_id')
        shares = request.data.get('shares')
        price = request.data.get('price')

        if not all([stock_id, shares, price]):
            return Response(
                {'error': 'Missing required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stock = get_object_or_404(Stock, id=stock_id)
        
        portfolio_stock, created = PortfolioStock.objects.get_or_create(
            portfolio=portfolio,
            stock=stock,
            defaults={
                'shares': shares,
                'average_price': price
            }
        )

        if not created:
            # Update existing position
            total_shares = float(portfolio_stock.shares) + float(shares)
            total_cost = (float(portfolio_stock.shares) * float(portfolio_stock.average_price) +
                         float(shares) * float(price))
            portfolio_stock.shares = total_shares
            portfolio_stock.average_price = total_cost / total_shares
            portfolio_stock.save()

        # Create transaction record
        Transaction.objects.create(
            portfolio=portfolio,
            stock=stock,
            transaction_type='BUY',
            shares=shares,
            price_per_share=price
        )

        return Response(PortfolioStockSerializer(portfolio_stock).data)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def prices(self, request, pk=None):
        stock = self.get_object()
        prices = stock.prices.all().order_by('-date')[:30]  # Last 30 days
        return Response(StockPriceSerializer(prices, many=True).data)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(portfolio__user=self.request.user)

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
