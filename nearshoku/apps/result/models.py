from django.db import models


class BaseModel(models.Model):
    """
    Base abstract model-form class with common methods
    """
    def save(self, *args, **kwargs):
        """
        A function to save modelform
        """
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ShopInfoModel(BaseModel):
    """
    A model-form to save shop info to show on result field
    """
    shop_id = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=100)
    shop_kana = models.CharField(max_length=100)
    shop_access = models.CharField(max_length=100)
    shop_thumbnail = models.ImageField()
    #shop_model_hash = models.CharField(max_length=50) # To verify the shown data
    searched_lat = models.FloatField() # To verify the shown data
    searched_lng = models.FloatField() # To verify the shown data

class ShopDetailModel(BaseModel):
    """
    A model-form to save shop info to show on detail field
    """
    #
    detail_shop_id = models.CharField(max_length=20)
    # 필수
    detail_name = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100)
    detail_image = models.ImageField() # photo:pc:l/m/s
    detail_time = models.CharField(max_length=100) #open
    #추가정보
    detail_kana = models.CharField(max_length=100)
    detail_access = models.CharField(max_length=100)
    detail_shop_memo = models.CharField(max_length=100,null=True)
    detail_budget_memo = models.CharField(max_length=100,null=True)
    detail_lat = models.FloatField()
    detail_lng = models.FloatField()
    detail_url = models.CharField(max_length=100, null=True) # urls:pc
    detail_card = models.CharField(max_length=10, null=True)
    detail_genre = models.CharField(max_length=50, null=True)
    detail_genre_catch = models.CharField(max_length=50, null=True)
    detail_price_average = models.CharField(max_length=50, null=True)
    detail_station = models.CharField(max_length=30, null=True)




class UserInfoModel(BaseModel):
    '''
    A model-form to save user info
    '''
    #user_model_hash = models.CharField(max_length=20)
    current_lat = models.FloatField() # => searched_lat
    current_lng = models.FloatField() # => searched_lng
    selected_lat = models.FloatField(null=True)
    selected_lng = models.FloatField(null=True)
    range = models.IntegerField()
    order = models.IntegerField()