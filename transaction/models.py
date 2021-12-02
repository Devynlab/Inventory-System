from django.db import models
from inventory.models import Stock

from . import utils


class Supplier(models.Model):
  supplier_id = models.CharField(max_length=15, default=utils.random_string, editable=False, unique=True)
  name = models.CharField(max_length=150)
  phone = models.CharField(max_length=12, unique=True)
  address = models.CharField(max_length=200)
  email = models.EmailField(max_length=254, unique=True)
  is_deleted = models.BooleanField(default=False)

  def __str__(self):
    return self.name


class PurchaseBill(models.Model):
  billno = models.AutoField(primary_key=True, unique=True)
  time = models.DateTimeField(auto_now=True)
  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchasesupplier')

  def __str__(self):
    return f"Bill no: {self.billno}"

  def get_items_list(self):
    return PurchaseItem.objects.filter(billno=self)

  def get_total_price(self):
    purchaseitems = PurchaseItem.objects.filter(billno=self)
    return sum(item.totalprice for item in purchaseitems)


class PurchaseItem(models.Model):
  billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasebillno')
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='purchaseitem')
  quantity = models.IntegerField(default=1)
  perprice = models.IntegerField(default=1)
  totalprice = models.IntegerField(default=1)

  def __str__(self):
    return f"Bill no: {self.billno.billno}, Item {self.stock.name}"


class PurchaseBillDetail(models.Model):
  billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasedetailsbillno')
  destination = models.CharField(max_length=50, blank=True, null=True)
  total = models.CharField(max_length=50, blank=True, null=True)

  def __str__(self):
    return f"Bill no: {self.billno.billno}"


class SaleBill(models.Model):
  billno = models.AutoField(primary_key=True, unique=True)
  time = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=150)
  phone = models.CharField(max_length=10)
  address = models.CharField(max_length=200)
  email = models.EmailField(max_length=254)
  sale_bill_id = models.CharField(max_length=15, default=utils.random_string, editable=False, unique=True)

  def __str__(self):
    return f"Bill no: {self.billno}"

  def get_items_list(self):
    return SaleItem.objects.filter(billno=self)

  def get_total_price(self):
    saleitems = SaleItem.objects.filter(billno=self)
    return sum(item.totalprice for item in saleitems)


class SaleItem(models.Model):
  billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='salebillno')
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='saleitem')
  quantity = models.IntegerField(default=1)
  perprice = models.IntegerField(default=1)
  totalprice = models.IntegerField(default=1)

  def __str__(self):
    return f"Bill no: {self.billno.billno}, Item = {self.stock.name}"

class SaleBillDetail(models.Model):
  billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='saledetailsbillno')
  destination = models.CharField(max_length=50, blank=True, null=True)
  total = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"Bill no: {self.billno.billno}"
