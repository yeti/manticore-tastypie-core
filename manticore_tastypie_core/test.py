from PIL import Image
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.utils.encoding import force_text
import json
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase


class ManticomResourceTestCase(ResourceTestCase):
    def setUp(self):
        super(ManticomResourceTestCase, self).setUp()

        # Parse schema objects for use later
        self.schema_objects = {}
        with open(settings.MANTICOM_SCHEMA) as file:
            schema_data = json.loads(file.read())
            for schema_obj in schema_data["objects"]:
                self.schema_objects.update(schema_obj)

    def get_authentication(self, user):
        api_key, created = ApiKey.objects.get_or_create(user=user)
        return self.create_apikey(user.email, api_key.key)

    def check_schema_keys(self, data_object, schema_fields):
        """
            `data_object` is the actual JSON being sent or received
            `schema_fields` is the expected JSON based on the schema file
        """
        required_fields = []

        for schema_field, schema_type in schema_fields.iteritems():
            # If this field is actually another related object, then check that object's fields as well
            schema_parts = schema_type.split(',')
            is_list = False
            is_optional = False
            new_schema_object = None
            for part in schema_parts:
                # Parse through all parts, regardless of ordering
                if part == "array":
                    is_list = True
                elif part == "optional":
                    is_optional = True
                elif part.startswith('$'):
                    new_schema_object = part

            if not is_optional:
                required_fields.append(schema_field)

            if new_schema_object:
                new_data_object = data_object[schema_field]
                if new_data_object is None:
                    # If our new object to check is None and optional then continue, else raise an error
                    if is_optional:
                        continue
                    else:
                        raise self.failureException("No data for object {0}".format(new_schema_object))
                elif is_list:
                    # If our new object to check is a list of these objects, continue if we don't have any daa
                    # Else grab the first one in the list
                    if len(new_data_object) == 0:
                        continue
                    new_data_object = new_data_object[0]

                self.check_schema_keys(new_data_object, self.schema_objects[new_schema_object])

        # The actual `data_object` contains every required field
        self.assertTrue(set(required_fields).issubset(set(data_object)))

        # The actual `data_object` contains no extraneous fields not found in the schema
        self.assertTrue(set(data_object).issubset(set(schema_fields)))

    def assertManticomGETResponse(self, url, key_path, response_object_name, user, **kwargs):
        """
            Takes a url, key path, and object name to run a GET request and
            check the results match the manticom schema
        """
        response = self.api_client.get("{}{}/".format(settings.API_PREFIX, url),
                                       authentication=self.get_authentication(user), **kwargs)
        self.assertValidJSONResponse(response)

        data = self.deserialize(response)[key_path]
        if len(data) == 0:
            raise self.failureException("No data to compare response")

        self.check_schema_keys(data[0], self.schema_objects[response_object_name])

    def assertManticomPOSTResponse(self, url, request_object_name, response_object_name, data, user, key_path=None):
        """
            Runs a POST request and checks the POST data and results match the manticom schema
        """
        self.assertKeys(data, self.schema_objects[request_object_name])
        response = self.api_client.post("{}{}/".format(settings.API_PREFIX, url), data=data,
                                        authentication=self.get_authentication(user))
        self.assertHttpCreated(response)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        self.assertValidJSON(force_text(response.content))

        data = self.deserialize(response)
        if 'meta' in data:  # If the POST returns a tastypie list, process looking for the first item
            data = data[key_path]
            if len(data) == 0:
                raise self.failureException("No data to compare response")
            self.assertKeys(data[0], self.schema_objects[response_object_name])
        else:
            self.assertKeys(data, self.schema_objects[response_object_name])

    def assertManticomPATCHResponse(self, url, request_object_name, response_object_name, data, user, **kwargs):
        """
            Runs a PATCH request and checks the PATCH data and results match the manticom schema
        """
        self.check_schema_keys(data, self.schema_objects[request_object_name])
        response = self.api_client.patch("{}{}/".format(settings.API_PREFIX, url), data=data,
                                         authentication=self.get_authentication(user), **kwargs)
        self.assertHttpAccepted(response)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        self.assertValidJSON(force_text(response.content))

        data = self.deserialize(response)
        self.assertKeys(data, self.schema_objects[response_object_name])

    def assertPhotoUpload(self, url, obj_to_update, user, path_to_image):
        """
            Checks that the photo is uploaded, saved, and resized
        """
        kwargs = {
            'HTTP_AUTHORIZATION': self.get_authentication(user),
            'data': {'picture': open(settings.PROJECT_ROOT + path_to_image, 'r')}
        }
        response = self.api_client.client.post("{}{}/upload_picture/{}/".format(settings.API_PREFIX,
                                                url,
                                                obj_to_update.pk),
                                               **kwargs
        )

        self.assertHttpAccepted(response)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        self.assertValidJSON(force_text(response.content))

        # Check the photo is saved
        obj_to_update = obj_to_update.__class__.objects.get(pk=obj_to_update.pk)
        self.assertEqual(
            obj_to_update.original_photo.file.read(),
            open(settings.PROJECT_ROOT + path_to_image, 'r').read()
        )

        # Check the photo is correctly resized
        for size_field, size in obj_to_update.__class__.SIZES.iteritems():
            w, h = get_image_dimensions(getattr(obj_to_update, size_field))
            self.assertEqual(size['height'], h)
            self.assertEqual(size['width'], w)
