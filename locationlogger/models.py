from django.db import models

class Location(models.Model):
    lat = models.DecimalField('latitude',decimal_places=6,max_digits=8)
    lon = models.DecimalField('longitude',decimal_places=6,max_digits=9)
    accuracy = models.DecimalField('accuracy (meters)',decimal_places=2,max_digits=8)
    update_time = models.DateTimeField("last updated")
