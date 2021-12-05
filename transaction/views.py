from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from inventory.models import Stock

from . import forms, models


class SupplierListView(generic.ListView):
  model = models.Supplier
  template_name = "suppliers/suppliers_list.html"
  queryset = models.Supplier.objects.filter(is_deleted=False)
  paginate_by = 10


class SupplierCreateView(SuccessMessageMixin, generic.CreateView):
  model = models.Supplier
  form_class = forms.SupplierForm
  success_url = '/transaction/suppliers'
  success_message = "Supplier has been created successfully"
  template_name = "suppliers/supplier-form.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'New Supplier'
    context["save_btn"] = 'Add'
    return context


class SupplierUpdateView(SuccessMessageMixin, generic.UpdateView):
  model = models.Supplier
  form_class = forms.SupplierForm
  success_url = '/transaction/suppliers'
  success_message = "Supplier details has been updated successfully"
  template_name = "suppliers/supplier-form.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Edit Supplier'
    context["save_btn"] = 'Save'
    context["del_btn"] = 'Delete'
    return context


class SupplierDeleteView(generic.View):
  template_name = "suppliers/delete_supplier.html"
  success_message = "Supplier has been deleted successfully"

  def get(self, request, pk):
    supplier = get_object_or_404(models.Supplier, pk=pk)
    return render(request, self.template_name, {'object': supplier})

  def post(self, request, pk):
    supplier = get_object_or_404(models.Supplier, pk=pk)
    supplier.is_deleted = True
    supplier.save()
    messages.success(request, self.success_message)
    return redirect('suppliers-list')


class SupplierView(generic.View):
  def get(self, request, name):
    supplierobj = get_object_or_404(models.Supplier, name=name)
    bill_list = models.PurchaseBill.objects.filter(supplier=supplierobj)
    page = request.GET.get('page', 1)
    paginator = Paginator(bill_list, 10)
    try:
      bills = paginator.page(page)
    except PageNotAnInteger:
      bills = paginator.page(1)
    except EmptyPage:
      bills = paginator.page(paginator.num_pages)
    context = {
      'supplier': supplierobj,
      'bills': bills
    }
    return render(request, 'suppliers/supplier.html', context)


class PurchaseListView(generic.ListView):
  model = models.PurchaseBill
  template_name = "purchases/purchases_list.html"
  context_object_name = 'bills'
  ordering = ['-time']
  paginate_by = 10


class SelectSupplierView(generic.View):
  form_class = forms.SelectSupplierForm
  template_name = 'purchases/select_supplier.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class
    return render(request, self.template_name, {'form': form})

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      supplierid = request.POST.get("supplier")
      supplier = get_object_or_404(models.Supplier, id=supplierid)
      return redirect('new-purchase', supplier.pk)
    return render(request, self.template_name, {'form': form})


class PurchaseCreateView(generic.View):
  template_name = 'purchases/new_purchase.html'

  def get(self, request, pk):
    formset = forms.PurchaseItemFormset(request.GET or None)
    supplier_obj = get_object_or_404(models.Supplier, pk=pk)
    context = {
      'formset': formset,
      'supplier': supplier_obj,
    }
    return render(request, self.template_name, context)

  def post(self, request, pk):
    formset = forms.PurchaseItemFormset(request.POST)
    supplier_obj = get_object_or_404(models.Supplier, pk=pk)
    if formset.is_valid():
      billobj = models.PurchaseBill(supplier=supplier_obj)
      billobj.save()
      billdetails_obj = models.PurchaseBillDetail(billno=billobj)
      billdetails_obj.save()
      for form in formset:
        billitem = form.save(commit=False)
        billitem.billno = billobj
        stock = get_object_or_404(Stock, name=billitem.stock.name)
        billitem.totalprice = billitem.perprice * billitem.quantity
        stock.quantity += billitem.quantity
        stock.save()
        billitem.save()
      messages.success(request, "Purchased items have been registered successfully")
      return redirect('purchase-bill', billno=billobj.billno)
    formset = forms.PurchaseItemFormset(request.GET or None)
    context = {
      'formset': formset,
      'supplier': supplier_obj
    }
    return render(request, self.template_name, context)


class PurchaseDeleteView(SuccessMessageMixin, generic.DeleteView):
  model = models.PurchaseBill
  template_name = "purchases/delete_purchase.html"
  success_url = '/transaction/purchases'

  def delete(self, *args, **kwargs):
    self.object = self.get_object()
    items = models.PurchaseItem.objects.filter(billno=self.object.billno)
    for item in items:
      stock = get_object_or_404(Stock, name=item.stock.name)
      if stock.is_deleted == False:
        stock.quantity -= item.quantity
        stock.save()
    messages.success(self.request, "Purchase bill has been deleted successfully")
    return super(PurchaseDeleteView, self).delete(*args, **kwargs)


class SaleView(generic.ListView):
  model = models.SaleBill
  template_name = "sales/sales_list.html"
  context_object_name = 'bills'
  ordering = ['-time']
  paginate_by = 10


class SaleCreateView(generic.View):
  template_name = 'sales/new_sale.html'

  def get(self, request):
    form = forms.SaleForm(request.GET or None)
    formset = forms.SaleItemFormset(request.GET or None)
    stock = Stock.objects.filter(is_deleted=False)
    context = {
      'form': form,
      'formset': formset,
      'stocks': stock
    }
    return render(request, self.template_name, context)

  def post(self, request):
    form = forms.SaleForm(request.POST)
    formset = forms.SaleItemFormset(request.POST)
    if form.is_valid() and formset.is_valid():
      billobj = form.save(commit=False)
      billobj.save()
      billdetails_obj = models.SaleBillDetail(billno=billobj)
      billdetails_obj.save()
      for form in formset:
        billitem = form.save(commit=False)
        billitem.billno = billobj
        stock = get_object_or_404(Stock, name=billitem.stock.name)
        billitem.totalprice = billitem.perprice * billitem.quantity
        stock.quantity -= billitem.quantity
        stock.save()
        billitem.save()
      messages.success(request, "Sold items have been registered successfully")
      return redirect('sale-bill', billno=billobj.billno)
    form = forms.SaleForm(request.GET or None)
    formset = forms.SaleItemFormset(request.GET or None)
    context = {
      'form': form,
      'formset': formset,
    }
    return render(request, self.template_name, context)


class SaleDeleteView(SuccessMessageMixin, generic.DeleteView):
  model = models.SaleBill
  template_name = "sales/delete_sale.html"
  success_url = '/transaction/sales'

  def delete(self, *args, **kwargs):
    self.object = self.get_object()
    items = models.SaleItem.objects.filter(billno=self.object.billno)
    for item in items:
      stock = get_object_or_404(Stock, name=item.stock.name)
      if stock.is_deleted == False:
        stock.quantity += item.quantity
        stock.save()
    messages.success(self.request, "Sale bill has been deleted successfully")
    return super(SaleDeleteView, self).delete(*args, **kwargs)


class PurchaseBillView(generic.View):
  model = models.PurchaseBill
  template_name = "bill/purchase_bill.html"
  bill_base = "bill/bill_base.html"

  def get(self, request, billno):
    aggregate_sum = models.PurchaseBill.objects.filter(billno=billno)
    context = {
      'aggregate_sum': aggregate_sum,
      'bill': models.PurchaseBill.objects.get(billno=billno),
      'items': models.PurchaseItem.objects.filter(billno=billno),
      'billdetails': models.PurchaseBillDetail.objects.get(billno=billno),
      'bill_base': self.bill_base,
    }
    return render(request, self.template_name, context)

  def post(self, request, billno):
    form = forms.PurchaseDetailsForm(request.POST)
    if form.is_valid():
      billdetails_obj = models.PurchaseBillDetail.objects.get(billno=billno)
      billdetails_obj.destination = request.POST.get("destination")
      billdetails_obj.total = request.POST.get("total")
      billdetails_obj.save()
      messages.success(request, "Bill details have been modified successfully")
    context = {
      'bill': models.PurchaseBill.objects.get(billno=billno),
      'items': models.PurchaseItem.objects.filter(billno=billno),
      'billdetails': models.PurchaseBillDetail.objects.get(billno=billno),
      'bill_base': self.bill_base,
    }
    return render(request, self.template_name, context)


class SaleBillView(generic.View):
  model = models.SaleBill
  template_name = "bill/sale_bill.html"

  def get(self, request, billno):
    items = models.SaleItem.objects.filter(billno=billno).values_list('totalprice', flat=True)
    aggregate_sum = sum(items)
    vat = aggregate_sum * 0.06
    goods = aggregate_sum - vat
    context = {
      'vat': vat,
      'goods': goods,
      'total_price': items,
      'aggregate_sum': aggregate_sum,
      'items': models.SaleItem.objects.filter(billno=billno),
      'bill': models.SaleBill.objects.get(billno=billno),
      'billdetails': models.SaleBillDetail.objects.get(billno=billno)
    }
    return render(request, self.template_name, context)

  def post(self, request, billno):
    form = forms.SaleDetailsForm(request.POST)
    if form.is_valid():
      billdetails_obj = models.SaleBillDetail.objects.get(billno=billno)
      billdetails_obj.destination = request.POST.get("destination")
      billdetails_obj.total = request.POST.get("total")
      billdetails_obj.save()
      messages.success(request, "Bill details have been modified successfully")
    context = {
      'items': models.SaleItem.objects.filter(billno=billno),
      'bill': models.SaleBill.objects.get(billno=billno),
      'billdetails': models.SaleBillDetail.objects.get(billno=billno),
    }
    return render(request, self.template_name, context)
