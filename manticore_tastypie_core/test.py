from django.conf import settings
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
        self.assertKeys(data[0], self.schema_objects[response_object_name])

    def assertManticomPOSTResponse(self, url, request_object_name, response_object_name, data, user, key_path=None):
        """
            Takes a url, key path, and object name to run a GET request and
            check the results match the manticom schema
        """
        self.assertKeys(data, self.schema_objects[request_object_name])
        response = self.api_client.post("{}{}/".format(settings.API_PREFIX, url),
                                        data=data,
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
