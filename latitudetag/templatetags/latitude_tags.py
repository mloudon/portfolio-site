from django import template
import urllib
import urllib2
import json
import datetime

import logging
logger = logging.getLogger("latitudetag")

register = template.Library()

def do_latitude_public_badge_request(userkey):
    try:
        url = "https://latitude.google.com/latitude/apps/badge/api"
        data = {}
        data["user"] = userkey
        data["type"] = "json"
        url_values = urllib.urlencode(data)
        full_url = url + "?" + url_values
        response = urllib2.urlopen(full_url)
        json_str = response.read()
    except URLError, e:
        json_str = ""
        if hasattr(e, 'reason'):
            logger.error("latitude public location fetch for user key %s failed; reason was %s" % (userkey, e.reason))
        elif hasattr(e, 'code'):
            logger.error("server error in latitude public location fetch for user key %s; error code was %s" % (userkey, e.code))
    
    return json_str
    
def get_params(token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, userkey = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    else:
        return userkey

@register.tag(name="latitude_json")
def get_latitude_json(parser, token):
    userkey = get_params(token)
    json_str = do_latitude_public_badge_request(userkey)
    return LatitudeNode("latitude_data",json_str)

@register.tag(name="get_latitude_data")
def get_latitude_data(parser, token):
    userkey = get_params(token)
    json_str = do_latitude_public_badge_request(userkey)
        
    #check if we actually got something back from the request
    if json_str == "":
        return LatitudeNode("latitude_data",{})
    try:
        features_str = json.loads(json_str)
    except ValueError: # could not decode the string as json
        return LatitudeNode("latitude_data",{})
    
    #check if the response contains a feature
    if ("features" not in features_str or len(features_str["features"])==0):
        return LatitudeNode("latitude_data",{})
    
    my_loc = features_str["features"][0]
 
    coords = my_loc["geometry"]["coordinates"]
    #weirdly, this is [lon, lat] - switch to lat,lon because this is what the static maps API uses
    coords_lat = coords[1]
    coords_lon = coords[0]
    
    loc_name = my_loc["properties"]["reverseGeocode"]
    
    timestamp = my_loc["properties"]["timeStamp"]
    lastseen_dt = datetime.datetime.fromtimestamp(timestamp)   
                        
    return LatitudeNode("latitude_data",{"coords_lat":coords_lat, "coords_lon":coords_lon,"loc_name":loc_name,"timestamp":timestamp,"lastseen": lastseen_dt})



class LatitudeNode(template.Node):
    def __init__(self, varname, result):
        self.varname = varname
        self.result = result
    def render(self, context):
        #maps visual_refresh
        context[self.varname] = self.result

        return ''