from django.conf import settings
from django.conf.urls import url
from django.db import IntegrityError
from django.db.models import FieldDoesNotExist
from tastypie import http, fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, Resource
from manticore_django.manticore_django.utils import retry_cloudfiles


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

    def update_in_place(self, request, original_bundle, new_data):
        """
            Set all FileFields to their relative path instead of their full url.
            This avoids trying to save their full url back to the database.
        """
        for field_name, value in original_bundle.data.iteritems():
            try:
                field_type = original_bundle.obj._meta.get_field(field_name).get_internal_type()
                if field_type == 'FileField':
                    original_bundle.data[field_name] = getattr(original_bundle.obj, field_name)
            except FieldDoesNotExist:
                pass

        super(ManticoreModelResource, self).update_in_place(request, original_bundle, new_data)


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
            obj = self._meta.queryset._clone().get(pk=kwargs['pk'])
        except self._meta.object_class.DoesNotExist:
            return http.HttpNotFound()

        bundle = self.build_bundle(obj=obj, request=request)

        self.authorized_update_detail(None, bundle)

        picture = request.FILES.get('picture', None)
        if not picture:
            return self.error_response(request, {"error": "No file called picture found"}, response_class=http.HttpBadRequest)

        def save_image(obj, picture):
            obj.original_photo.save(picture.name, picture)
            obj.save(update_fields=['original_photo'])

        retry_cloudfiles(save_image, bundle.obj, request.FILES['picture'])

        bundle = self.full_dehydrate(bundle)

        def return_response(resource, request, bundle):
            return resource.create_response(request, bundle, response_class=http.HttpAccepted)

        # Retry cloudfiles in case we get a 404 because the photos haven't finished uploading yet
        return retry_cloudfiles(return_response, self, request, bundle)

    def upload_video(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            obj = self._meta.queryset._clone().get(pk=kwargs['pk'])
        except self._meta.object_class.DoesNotExist:
            return http.HttpNotFound()

        bundle = self.build_bundle(obj=obj, request=request)

        self.authorized_update_detail(None, bundle)

        video = request.FILES.get('video', None)
        if not video:
            return self.error_response(request, {"error": "No file called video found"}, response_class=http.HttpBadRequest)

        video_thumbnail = request.FILES.get('video_thumbnail', None)
        if not video_thumbnail:
            return self.error_response(request, {"error": "No file called video_thumbnail found"}, response_class=http.HttpBadRequest)

        def save_video(obj, video):
            obj.video.save(video.name, video)
            obj.video_thumbnail.save(video_thumbnail.name, video_thumbnail)
            obj.save(update_fields=['video', 'video_thumbnail'])

        retry_cloudfiles(save_video, bundle.obj, video)

        bundle = self.full_dehydrate(bundle)

        def return_response(resource, request, bundle):
            return resource.create_response(request, bundle, response_class=http.HttpAccepted)

        # Retry cloudfiles in case we get a 404 because the videos haven't finished uploading yet
        return retry_cloudfiles(return_response, self, request, bundle)


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