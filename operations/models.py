from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

# Create your models here.
class Order(models.Model):
    gam_account_no = models.CharField(max_length=32, db_index=True)
    order_id = models.BigIntegerField(db_index=True)
    order_name = models.CharField(max_length=64, db_index=True, blank=True)
    advertiser = models.CharField(max_length=64, db_index=True, blank=True)
    trafficker = models.CharField(max_length=64, db_index=True, blank=True)

class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    li_id = models.BigIntegerField(db_index=True)
    li_name = models.CharField(max_length=64, db_index=True)
    li_price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    li_inventory = ArrayField(models.CharField(max_length=32, blank=True))
    li_geo = ArrayField(models.CharField(max_length=32, blank=True))
    li_custom_targeting = HStoreField()
    li_sizes = ArrayField(models.CharField(max_length=32, blank=True))
    li_status = models.CharField(max_length=12, blank=True)

class Group(models.Model):
    orders = models.ManyToManyField(Order, related_name="orders",
                                    blank=True)
    line_items = models.ManyToManyField(LineItem, related_name="line_items",
                                        blank=True)
    base_pql = models.CharField(max_length=255)


class Object(models.Model):
    name = models.CharField(max_length=255)
    gam_name = models.CharField(max_length=255)
