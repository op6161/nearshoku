from django.db import models

class ShopInfoModel(models.Model):
    '''
    A model-form to save shop info
    '''
    shop_list_number = models.IntegerField()
    shop_id = models.IntegerField()
    shop_name = models.CharField(max_length=100)
    shop_kana = models.CharField(max_length=100)
    shop_access = models.CharField(max_length=100)
    shop_thumbnail = models.ImageField()