from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    current_qte = models.PositiveIntegerField(default=0)
    measure_unit = models.CharField(max_length=10)
    active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
