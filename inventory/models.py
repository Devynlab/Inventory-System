from django.db import models

class Stock(models.Model):
  name = models.CharField(max_length=30, unique=True)
  unit = models.CharField(max_length=5, default="PCS")
  quantity = models.PositiveIntegerField(default=0, editable=False)
  brand = models.CharField(max_length=30, default="Generic")
  is_deleted = models.BooleanField(default=False)

  class Meta:
    verbose_name_plural = 'Stock'

  def __str__(self):
    return self.name
