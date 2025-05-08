from django.db import models

class DateDim(models.Model):
    date_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()

    class Meta:
        db_table = 'date_dim'

class StoreDim(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=100)

    class Meta:
        db_table = 'store_dim'

class PromotionDim(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_type = models.CharField(max_length=100)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'promotion_dim'
