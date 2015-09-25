from _ssl import SSLError
from django.conf import settings
from django.conf.urls import url
from django.db import IntegrityError
from googleplaces import GooglePlaces
from tastypie import http, fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, Resource
from manticore_tastypie_core.manticore_tastypie_core.models import Location
from manticore_tastypie_user.manticore_tastypie_user.authentication import ExpireApiKeyAuthentication


class BaseModelResource(ModelResource):
    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        """
        Unfortunately we must override this method because tastypie ignores 'blank' attribute
        on model fields.

        Here we invoke an insane workaround hack due to metaclass inheritance issues:
            http://stackoverflow.com/questions/12757468/invoking-super-in-classmethod-called-from-metaclass-new
        """
        this_class = next(c for c in cls.__mro__ if c.__module__ == __name__ and c.__name__ == 'BaseModelResource')
        fields = super(this_class, cls).get_fields(fields=fields, excludes=excludes)
        if not cls._meta.object_class:
            return fields
        for django_field in cls._meta.object_class._meta.fields:
            if django_field.blank == True:
                res_field = fields.get(django_field.name, None)
                if res_field:
                    res_field.blank = True
        return fields


class ManticoreModelResource(BaseModelResource):

    def alter_list_data_to_serialize(self, request, data):
        if hasattr(self._meta, 'object_name'):
            data[self._meta.object_name] = data['objects']
            del data['objects']
        return data

    def alter_deserialized_list_data(self, request, data):
        if hasattr(self._meta, 'object_name'):
            data['objects'] = data[self._meta.object_name]
            del data[self._meta.object_name]
        return data

    def obj_create(self, bundle, **kwargs):
        try:
            return super(ManticoreModelResource, self).obj_create(bundle, **kwargs)
        except IntegrityError, e:
            if 'duplicate key' in e.message:
                raise BadRequest("This object already exists and would violate a unique key constraint")
            else:
                raise e


class ManticoreResource(Resource):

    def alter_list_data_to_serialize(self, request, data):
        if hasattr(self._meta, 'object_name'):
            data[self._meta.object_name] = data['objects']
            del data['objects']
        return data

    def alter_deserialized_list_data(self, request, data):
        if hasattr(self._meta, 'object_name'):
            data['objects'] = data[self._meta.object_name]
            del data[self._meta.object_name]
        return data


class PictureVideoUploadResource(ManticoreModelResource):

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/upload_picture/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_picture'), name="api_upload_picture"),
            url(r"^(?P<resource_name>%s)/upload_video/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_video'), name="api_upload_video"),
        ]

    def upload_picture(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            report = self._meta.queryset._clone().get(pk=kwargs['pk'])
        except self._meta.object_class.DoesNotExist:
            return http.HttpNotFound()

        bundle = self.build_bundle(obj=report, request=request)

        self.authorized_update_detail(None, bundle)

        picture = request.FILES.get('picture', None)
        if not picture:
            return self.error_response(request, {"error": "No file called picture found"}, response_class=http.HttpBadRequest)

        picture = request.FILES['picture']

        done, tries = False, 0
        while not done:
            try:
                bundle.obj.original_photo.save(picture.name, picture)
                bundle.obj.save(update_fields=['original_photo'])
                done = True
            except SSLError:
                pass

            # Try at max, 10 times before quitting
            tries += 1
            if tries > 10:
                done = True

        bundle = self.full_dehydrate(bundle)

        return self.create_response(request, bundle, response_class=http.HttpAccepted)

    def upload_video(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            report = self._meta.queryset._clone().get(pk=kwargs['pk'])
        except self._meta.object_class.DoesNotExist:
            return http.HttpNotFound()

        bundle = self.build_bundle(obj=report, request=request)

        self.authorized_update_detail(None, bundle)

        video = request.FILES.get('video', None)
        if not video:
            return self.error_response(request, {"error": "No file called video found"}, response_class=http.HttpBadRequest)

        video_thumbnail = request.FILES.get('video_thumbnail', None)
        if not video_thumbnail:
            return self.error_response(request, {"error": "No file called video_thumbnail found"}, response_class=http.HttpBadRequest)

        done, tries = False, 0
        while not done:
            try:
                bundle.obj.video.save(video.name, video)
                bundle.obj.video_thumbnail.save(video_thumbnail.name, video_thumbnail)
                bundle.obj.save(update_fields=['video', 'video_thumbnail'])
                done = True
            except SSLError:
                pass

            # Try at max, 10 times before quitting
            tries += 1
            if tries > 10:
                done = True

        bundle = self.full_dehydrate(bundle)
        return self.create_response(request, bundle, response_class=http.HttpAccepted)


class GooglePlace(object):
    def __init__(self, id=None, name=None, address=None):
        self.id = id
        self.name = name
        self.address = address


class GooglePlaceResource(ManticoreResource):
    id = fields.CharField(attribute='id')
    name = fields.CharField(attribute='name')
    address = fields.CharField(attribute='vicinity', null=True)
    latitude = fields.FloatField()
    longitude = fields.FloatField()

    class Meta:
        resource_name = 'place'
        allowed_methods = ['get']
        object_class = GooglePlace
        authorization = Authorization()
        authentication = ExpireApiKeyAuthentication()
        always_return_data = True
        object_name = "place"

    def dehydrate_latitude(self, bundle):
        return bundle.obj.geo_location['lat']

    def dehydrate_longitude(self, bundle):
        return bundle.obj.geo_location['lng']

    def _client(self):
        return GooglePlaces(settings.GOOGLE_API_KEY)

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj['id']

        return kwargs

    def get_object_list(self, bundle, **kwargs):
        latitude = bundle.request.GET.get('latitude')
        longitude = bundle.request.GET.get('longitude')

        if latitude and longitude:
            lat_lng = {"lat": latitude, "lng": longitude}
        else:
            raise BadRequest("Need latitude and longitude")

        query_name = bundle.request.GET.get('query', "")
        if query_name != "":
            query = self._client().text_search(query=query_name, radius=None)
        else:
            query = self._client().nearby_search(sensor=True, lat_lng=lat_lng, radius=8000)

        return query.places

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle, **kwargs)

    def obj_get(self, request=None, **kwargs):
        result = self._client().get_place(kwargs['pk'])
        result.get_details()
        return result


class LocationResource(ManticoreModelResource):
    class Meta:
        queryset = Location.objects.all()
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        authentication = ExpireApiKeyAuthentication()
        resource_name = "location"
        object_name = "location"
        filtering = {
            'id': ['exact'],
            'name': ['exact'],
            'neighborhood': ['exact'],
            'city': ['exact'],
            'state': ['exact'],
            'country_code': ['exact', 'iexact'],
        }


class Version(object):
    def __init__(self, identifier=None):
        self.identifier = identifier


class VersionResource(ManticoreResource):
    identifier = fields.CharField(attribute='identifier')

    class Meta:
        resource_name = 'version'
        allowed_methods = ['get']
        object_class = Version
        authorization = Authorization()
        authentication = Authentication()
        object_name = "version"

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.identifier
        else:
            kwargs['pk'] = bundle_or_obj['identifier']

        return kwargs

    def get_object_list(self, bundle, **kwargs):
        return [Version(identifier=settings.VERSION)]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle, **kwargs)