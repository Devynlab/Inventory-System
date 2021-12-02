import django_filters

from . import models

class StockFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = models.Stock
    fields = ['name']
