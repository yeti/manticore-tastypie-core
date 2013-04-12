from django.conf.urls import url
from tastypie import http
from tastypie.resources import ModelResource, Resource


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


class PictureUploadResource(ManticoreModelResource):

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/upload_picture/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_picture'), name="api_upload_picture"),
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
        bundle.obj.original_photo.save(picture.name, picture)
        bundle.obj.save(update_fields=['original_photo'])

        # bundle = self.build_bundle(obj=report, request=request)
        bundle = self.full_dehydrate(bundle)

        return self.create_response(request, bundle, response_class=http.HttpAccepted)