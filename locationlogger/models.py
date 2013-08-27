from django.db import models
from pygeocoder import Geocoder
from decimal import *


class Location(models.Model):
    lat = models.DecimalField('latitude',decimal_places=6,max_digits=8)
    lon = models.DecimalField('longitude',decimal_places=6,max_digits=9)
    accuracy = models.DecimalField('accuracy (meters)',decimal_places=2,max_digits=8)
    update_time = models.DateTimeField("last updated")
    city_str = models.TextField(default="Unknown Location")
    city_lat = models.DecimalField('city_level_latitude',decimal_places=6,max_digits=8)
    city_lon = models.DecimalField('city_level_longitude',decimal_places=6,max_digits=9)
    
    def save(self, *args, **kwargs):
        latlon = (self.lat.quantize(Decimal(10) ** -3).normalize(), self.lon.quantize(Decimal(10) ** -3).normalize())
        city = "Unknown Location"
        
        print "Geocoder.reverse_geocode(%s,%s)" % (self.lat, self.lon)
        address = Geocoder.reverse_geocode(self.lat, self.lon)
        if (address):
            city = "%s, %s, %s" % (address[0].locality,address[0].state,address[0].country)
            print city
            latlon = Geocoder.geocode(city).coordinates
            print latlon
        
        self.city_lat = latlon[0]
        self.city_lon = latlon[1]
        self.city_str = city
        
        super(Location, self).save(*args, **kwargs)
    
    class Meta:
        get_latest_by = "update_time"
        
    
