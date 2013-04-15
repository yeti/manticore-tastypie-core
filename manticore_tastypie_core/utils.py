from manticore_tastypie_core.manticore_tastypie_core.resources import GooglePlaceResource, LocationResource

__author__ = 'rudolphmutter'


# Registers this library's resources
def register_api(api):
    api.register(GooglePlaceResource())
    api.register(LocationResource())
    return api