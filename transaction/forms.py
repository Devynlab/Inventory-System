from django import forms
from django.forms import formset_factory
from inventory.models import Stock

from . import models


class SelectSupplierForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['supplier'].queryset = models.Supplier.objects.filter(is_deleted=False)
    self.fields['supplier'].widget.attrs.update({'class': 'form-control'})

  class Meta:
    model = models.PurchaseBill
    fields = ['supplier']


class PurchaseItemForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
    self.fields['stock'].widget.attrs.update({'class': 'form-control setprice stock', 'required': 'true'})
    self.fields['quantity'].widget.attrs.update({'class': 'form-control setprice quantity', 'min': '0', 'required': 'true'})
    self.fields['perprice'].widget.attrs.update({'class': 'form-control setprice price', 'min': '0', 'required': 'true'})

  class Meta:
    model = models.PurchaseItem
    fields = ['stock', 'quantity', 'perprice']


PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)


class PurchaseDetailsForm(forms.ModelForm):
  class Meta:
    model = models.PurchaseBillDetail
    fields = '__all__'


class SupplierForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs.update({'class': 'form-control', 'pattern': '[a-zA-Z\s]{1,50}', 'title': 'Alphabets and Spaces only'})
    self.fields['phone'].widget.attrs.update({'class': 'form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
    self.fields['email'].widget.attrs.update({'class': 'form-control'})

  class Meta:
    model = models.Supplier
    fields = ['name', 'phone', 'address', 'email']
    widgets = {
      'address': forms.Textarea(
        attrs={
          'class': 'form-control',
          'rows': '4'
        }
      )
    }


class SaleForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs.update({'class': 'form-control', 'pattern': '[a-zA-Z\s]{1,50}', 'title': 'Alphabets and Spaces only', 'required': 'true'})
    self.fields['phone'].widget.attrs.update({'class': 'form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only', 'required': 'true'})
    self.fields['email'].widget.attrs.update({'class': 'form-control'})

  class Meta:
    model = models.SaleBill
    fields = ['name', 'phone', 'address', 'email']
    widgets = {
      'address': forms.Textarea(
        attrs={
          'class': 'form-control',
          'rows': '4'
        }
      )
    }


class SaleItemForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
    self.fields['stock'].widget.attrs.update({'class': 'form-control setprice stock', 'required': 'true'})
    self.fields['quantity'].widget.attrs.update({'class': 'form-control setprice quantity', 'min': '1', 'required': 'true'})
    self.fields['perprice'].widget.attrs.update({'class': 'form-control setprice price', 'min': '1', 'required': 'true'})

  class Meta:
    model = models.SaleItem
    fields = ['stock', 'quantity', 'perprice']


SaleItemFormset = formset_factory(SaleItemForm, extra=1)


class SaleDetailsForm(forms.ModelForm):
  class Meta:
    model = models.SaleBillDetail
    fields = '__all__'
