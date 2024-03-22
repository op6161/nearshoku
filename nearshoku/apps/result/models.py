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