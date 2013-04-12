from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.exceptions import ApiFieldError
from tastypie.fields import ToOneField


# Receives and Outputs ints representing primary keys of the field.
class ToBareForeignKeyField(ToOneField):

    def build_related_resource(self, value, request=None, related_obj=None, related_name=None):
        if not isinstance(value, int):
            raise ApiFieldError("The '%s' field was given non-integer data: %s." % (self.instance_name, value))

        self.fk_resource = self.to_class()

        #TODO: Dynamically pull api path
        value = "/api/v1/%s/%s/" % (self.fk_resource.Meta.resource_name, value)

        return super(ToBareForeignKeyField, self).build_related_resource(value, request, related_obj, related_name)

    def dehydrate(self, bundle):
        field_id_name = "%s_id" % self.attribute

        if hasattr(bundle.obj, field_id_name):
            value = getattr(bundle.obj, field_id_name)

            if not value:
                if not self.null:
                    raise ApiFieldError("The model '%r' has an empty attribute '%s' and doesn't allow a null value." % (bundle.obj, self.attribute))

                return None

            return value
        else:
            raise ApiFieldError("The model '%r' doesn't have an id for attribute '%s'" % (bundle.obj, self.attribute))


# Expects there to be only one model and resource pair in the generic foreign key
class BareGenericForeignKeyField(GenericForeignKeyField):

    def build_related_resource(self, value, request=None, related_obj=None, related_name=None):
        if not isinstance(value, int):
            raise ApiFieldError("The '%s' field was given non-integer data: %s." % (self.instance_name, value))

        #TODO: Dynamically pull api path)
        value = "/api/v1/%s/%s/" % (self.to.itervalues().next().Meta.resource_name, value)

        return super(BareGenericForeignKeyField, self).build_related_resource(value, request, related_obj, related_name)