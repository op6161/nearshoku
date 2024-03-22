from django.db import models

class ByCurrentModel(models.Model):
    current_lat = models.FloatField()
    current_lng = models.FloatField()
    current_range = models.IntegerField()


class BySelectedModel(models.Model):
    current_lat = models.FloatField()
    current_lng = models.FloatField()
    selected_lat = models.FloatField()
    selected_lng = models.FloatField()
    current_range = models.IntegerField()

class ShopInfoModel(models.Model):
    shop_id = models.IntegerField()
    shop_name = models.CharField(max_length=30)
    shop_url = models.CharField(max_length=30)

class ShopDetailsModel(models.Model):
    shop_id = models.IntegerField()