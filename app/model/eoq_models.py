from django.db import models
from django.contrib.auth.models import User as AppUser


class Product(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return f"product: {self.name} price: {self.price}"

class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    total_price = models.FloatField()
    status = models.CharField(max_length=255)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"order: {self.id} user: {self.user.username}"
