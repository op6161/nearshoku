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
    A model-form to save shop info
    """
    shop_id = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=100)
    shop_kana = models.CharField(max_length=100)
    shop_access = models.CharField(max_length=100)
    shop_thumbnail = models.ImageField()
    shop_model_hash = models.CharField(max_length=50) # To verify the shown data
    # shop_is_current = models.BooleanField()
    # 뒤로가기로 돌아가서 current/selected를 누르면 동일한 결과가 출력된다
    # 검증을 위한 데이터 추가가 필요



class UserInfoModel(BaseModel):
    '''
    A model-form to save user info
    '''
    user_model_hash = models.CharField(max_length=20)
    current_lat = models.FloatField()
    current_lng = models.FloatField()
    selected_lat = models.FloatField(null=True)
    selected_lng = models.FloatField(null=True)
    range = models.IntegerField()
    order = models.BooleanField()