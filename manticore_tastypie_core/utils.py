import math
from manticore_tastypie_core.manticore_tastypie_core.resources import GooglePlaceResource, LocationResource, VersionResource

__author__ = 'rudolphmutter'


# Registers this library's resources
def register_api(api):
    api.register(GooglePlaceResource())
    api.register(LocationResource())
    api.register(VersionResource())
    return api


# 111.12 km = 1 degree of latitude
# distance in km
# ref http://www.scribd.com/doc/2569355/Geo-Distance-Search-with-MySQL, slide 12
def get_longitude_range(longitude, latitude, dist):
    lon1 = longitude - dist / abs(math.cos(math.radians(latitude)) * 111.12)
    lon2 = longitude + dist / abs(math.cos(math.radians(latitude)) * 111.12)

    return lon1, lon2


def get_latitude_range(latitude, dist):
    lat1 = latitude - (dist / 111.12)
    lat2 = latitude + (dist / 111.12)

    return lat1, lat2