from django import forms

from . import models

class StockForm(forms.ModelForm):
  class Meta:
    model = models.Stock
    fields = ['name', 'unit', 'brand']
    widgets = {
      'name': forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Name'
      }),
      'unit': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Unit'
      }),
      'brand': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Brand'
      })
    }
