from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    description = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    seller_id = models.CharField(max_length=255, null=True, blank=True)
    in_stock = models.BooleanField(null=True, blank=True)

    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DeliveryOptions(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, related_name="delivery_options", related_query_name='delivery_options',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name
