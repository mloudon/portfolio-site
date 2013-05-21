from django import template
import urllib
import urllib2
import json

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
    return LatitudeNode(json_str)

@register.tag(name="latitude_coords")
def get_latitude_coords(parser, token):
    userkey = get_params(token)
    json_str = do_latitude_public_badge_request(userkey)
    
    render_str = ""
    
    #check if we actually got something back from the request
    if json_str != "":
        features_str = json.loads(json_str)
    
        #check if the response contains a feature
        if ("features" in features_str and len(features_str["features"])>0):
            my_loc = features_str["features"][0]
            coords = my_loc["geometry"]["coordinates"]
            render_str = "%s,%s" % (coords[1],coords[0]) 
                    
    return LatitudeNode(render_str)



class LatitudeNode(template.Node):
    def __init__(self, userkey):
        self.userkey = userkey
    def render(self, context):
        #maps visual_refresh
        return self.userkey