from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username if self.username else "None"


class Geo(models.Model):
    geo_name = models.CharField(max_length=255)

    def __str__(self):
        return self.geo_name


class Gram(models.Model):
    gram = models.FloatField()

    def __str__(self):
        return f"{self.gram}"


class Product(models.Model):
    geo_name = models.ForeignKey(Geo, on_delete=models.CASCADE)
    product_name = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    gram = models.ForeignKey(Gram, on_delete=models.CASCADE)
    byed_by = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()
    address = models.TextField()
    reserved = models.BooleanField(default=False)


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=255)

    def __str__(self):
        return self.chapter_name


class Invoice(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    req = models.TextField()
    ltc_sum = models.FloatField()
    active = models.BooleanField(default=True)
    reserved_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
