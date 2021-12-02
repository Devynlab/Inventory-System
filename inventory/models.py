from django.db import models

class Stock(models.Model):
  name = models.CharField(max_length=30, unique=True)
  unit = models.CharField(max_length=3, default="PCS")
  quantity = models.PositiveIntegerField(default=1)
  is_deleted = models.BooleanField(default=False)

  class Meta:
    verbose_name_plural = 'Stock'

  def __str__(self):
    return self.name
