from manticore_tastypie_core.manticore_tastypie_core.resources import VersionResource

__author__ = 'rudolphmutter'


# Registers this library's resources
def register_api(api):
    api.register(VersionResource())
    return api