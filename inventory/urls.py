from django.urls import path

from . import views

urlpatterns = [
  path('', views.StockListView.as_view(), name='inventory'),
  path('new', views.StockCreateView.as_view(), name='new-stock'),
  path('stock/edit/<pk>', views.StockUpdateView.as_view(), name='edit-stock'),
  path('stock/delete/<pk>', views.StockDeleteView.as_view(), name='delete-stock'),
]
