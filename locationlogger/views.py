from django.http import HttpResponse
import sys, json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from locationlogger.models import Location

import datetime
from django.utils.timezone import utc

from decimal import *

import logging

from mezzanine.utils.views import render

@csrf_exempt
def update_location(request):
    if request.method == "POST":
            logging.error("Raw Data: %s",request.body)
            try:
                loc_data = json.loads(request.body)
                logging.debug("json loaded")
                utc_date = datetime.datetime.fromtimestamp(float(loc_data["timestamp"]))
                logging.debug("utc date %s", utc_date)
                loc = Location.objects.create(lat=Decimal(loc_data["lat"]), lon=Decimal(loc_data["lon"]), 
                                              accuracy=Decimal(loc_data["acc"]), 
                                              update_time=utc_date)
                loc.save()
                logging.debug("saved location")
                return HttpResponse(status=201)
            except TypeError as e:
                logging.error("typeerror saving location, error was %s", e)
                return HttpResponse(status=400)
            except:
                logging.error("exception saving location, error was %s", sys.exc_info()[0])
                return HttpResponse(status=400)
    else:
        logging.error("update location view: not a POST request")
        return HttpResponse(status=400)
    
def last_known_loc(request, template="last_known_location.html"):
    last_loc = Location.objects.latest()
    
    context = {"last_seen_time": last_loc.update_time, "coords_lat": last_loc.city_lat, "coords_lon": last_loc.city_lon,
               "last_seen_loc_name": last_loc.city_str}
    return render(request, template, context)

@login_required
def last_known_loc_accurate(request, template="last_known_location.html"):
    last_loc = Location.objects.latest()
    
    context = {"last_seen_time": last_loc.update_time, "coords_lat": last_loc.lat, "coords_lon": last_loc.lon,
               "last_seen_loc_name": last_loc.city_str}
    return render(request, template, context)
    
