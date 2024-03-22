from django.db import models

class ShopInfoModel(models.Model):
    '''
    A model-form to save shop info
    '''
    shop_id = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=100)
    shop_kana = models.CharField(max_length=100)
    shop_access = models.CharField(max_length=100)
    shop_thumbnail = models.ImageField()
    shop_model_hash = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)