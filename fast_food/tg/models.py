from django.db import models

# Create your models here.
from django.utils.text import slugify


class Log(models.Model):
    user_id = models.BigIntegerField()
    messages = models.JSONField(default={'state': 0})


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=15, null=True)
    lang = models.IntegerField(null=True, default=1)
    menu = models.IntegerField(null=True, default=0)


class Category(models.Model):
    name_uz = models.CharField(max_length=56)
    name_ru = models.CharField(max_length=56)

    def __str__(self):
        return self.name_uz


class SubCategory(models.Model):
    name_uz = models.CharField(max_length=56)
    name_ru = models.CharField(max_length=56)
    ctg = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_uz


class Made_in1(models.Model):
    name_uz = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)
    subctg = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    name_uz = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)
    img = models.ImageField()
    made_in = models.ForeignKey(Made_in1, on_delete=models.SET_NULL, null=True)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_uz


class Savat(models.Model):
    product = models.CharField(max_length=256)
    til = models.IntegerField(default=1)
    user_id = models.BigIntegerField()
    slug = models.SlugField(max_length=128, null=True)
    narxi = models.IntegerField(null=True)
    summ = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product)

        return super(Savat, self).save(*args, **kwargs)

    def str(self):
        return self.product
