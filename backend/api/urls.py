from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'portfolios', views.PortfolioViewSet, basename='portfolio')
router.register(r'stocks', views.StockViewSet)
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'stock-prices', views.StockPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 