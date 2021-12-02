from django.shortcuts import render
from django.views import generic
from inventory.models import Stock
from transaction import models


class HomeView(generic.View):
  template_name = "home.html"

  def get(self, request):
    labels = []
    data = []
    stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
    for item in stockqueryset:
      labels.append(item.name)
      data.append(item.quantity)
    sales = models.SaleBill.objects.order_by('-time')[:3]
    purchases = models.PurchaseBill.objects.order_by('-time')[:3]
    context = {
      'labels': labels,
      'data': data,
      'sales': sales,
      'purchases': purchases
    }
    return render(request, self.template_name, context)


class AboutView(generic.TemplateView):
  template_name = "about.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    purchases = models.PurchaseItem.objects.all().values_list('totalprice', flat=True)
    total_purchases = sum(purchases)
    sales = models.SaleItem.objects.all().values_list('totalprice', flat=True)
    total_sales = sum(sales)
    total_inventory = total_purchases - total_sales
    context["purchases"] = total_purchases
    context["sales"] = total_sales
    context["inventory"] = total_inventory
    return context
