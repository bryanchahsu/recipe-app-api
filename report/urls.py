# reports/urls.py
from django.urls import path
from .views import SalesReport, SalesBySKUReport

urlpatterns = [
    path('reports/sales-report/', SalesReport.as_view(), name='sales-report'),
    path('reports/sales-by-sku/', SalesBySKUReport.as_view(), name='sales-by-sku-report'),

]
