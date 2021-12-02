from django.contrib import admin

from . import models

# @admin.register(models.PurchaseBill)
# class PurchaseBillAdmin(admin.ModelAdmin):
#   list_display = ['billno', 'time']

# @admin.register(models.PurchaseBillDetail)
# class PurchaseBillDetailsAdmin(admin.ModelAdmin):
#   list_display = ['billno', 'destination', 'total']

@admin.register(models.PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
  list_display = ['stock', 'quantity', 'perprice', 'totalprice']

@admin.register(models.SaleBill)
class SaleBillAdmin(admin.ModelAdmin):
  list_display = ['name', 'billno', 'time']

@admin.register(models.SaleBillDetail)
class SaleBillDetailsAdmin(admin.ModelAdmin):
  # list_display = ['destination', 'billno', 'total']
  pass

@admin.register(models.SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
  list_display = ['stock', 'billno', 'totalprice']

@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
  list_display = ['name', 'supplier_id', 'is_deleted']
