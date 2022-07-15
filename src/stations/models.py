from django.db import models

# Create your models here.

class station(models.Model):
    lat = models.CharField(max_length=45)
    longi = models.CharField(max_length=45)
    date_measure = models.CharField(max_length=45)
    hour_measure = models.CharField(max_length=45)
    gas_name = models.CharField(max_length=45)
    gas_measure = models.CharField(max_length=45)
    station_type = models.CharField(max_length=45)
    entry_date = models.CharField(max_length=45)
    origin_measure = models.CharField(max_length=45)

    class Meta:
        db_table = 'tfgdata2'
