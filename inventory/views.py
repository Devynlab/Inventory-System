from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from . import filters, forms, models


class StockListView(FilterView):
  filterset_class = filters.StockFilter
  queryset = models.Stock.objects.filter(is_deleted=False)
  template_name = 'inventories.html'
  paginate_by = 10


class StockCreateView(SuccessMessageMixin, generic.CreateView):
  model = models.Stock
  form_class = forms.StockForm
  template_name = "stock-form.html"
  success_url = reverse_lazy('inventory')
  success_message = "Stock has been created successfully"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'New Stock'
    context["save_btn"] = 'Add'
    return context


class StockUpdateView(SuccessMessageMixin, generic.UpdateView):
  model = models.Stock
  form_class = forms.StockForm
  template_name = "stock-form.html"
  success_url = reverse_lazy('inventory')
  success_message = "Stock has been updated successfully"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Edit'
    context["save_btn"] = 'Update'
    context["delete_btn"] = 'Delete'
    return context


class StockDeleteView(generic.View):
  template_name = "delete_stock.html"
  success_message = "Stock has been deleted successfully"

  def get(self, request, pk):
    stock = get_object_or_404(models.Stock, pk=pk)
    return render(request, self.template_name, {'object': stock})

  def post(self, request, pk):
    stock = get_object_or_404(models.Stock, pk=pk)
    stock.is_deleted = True
    stock.save()
    messages.success(request, self.success_message)
    return redirect('inventory')
