manticore-tastypie-core
=======================

Core functionality for using tastypie with manticore


Features :
----------

*   Custom Paginator



Requirements :
--------------

Prerequisities for running the script:


* `manticore-django`, which requires :
    * Python 2.6 or higher
    * `fabric`
    * `simplejson`
* `python-swiftclient`

----

### paginator.py

Class `StreamPaginator` sub-classes tastypie's `Paginator` :

StreamPaginator paginates calls by putting a created date filter on the query, if it doesn't already exists.
This removes the possibility of having duplicate objects sent down to the caller if a new object has been created
while paginating (therefore increasing the total count of this API call). 
It automatically adds a *created* filter to avoid this from happening.

Only works with resources with objects in descending order by `created`.

---

###  resources.py

- class `BaseModelResource(ModelResource)` : 
Upgrade to tastypie's ModelResouce class. Makes it possible not to ignore 'blank' attributes.


- class `ManticoreModelResource(BaseModelResource)` :
Simplify third-party interaction with the API by providing a meaningful JSON file.
Used with ORM Data Sources.

- class `ManticoreResource(Resource)` :
Simplify third-party interaction with the API by providing a meaningful JSON file.
For use with Non-ORM Data Source.

- class `PictureVideoUploadResource(ManticoreModelResource)` :
Provides all the resources for managing the upload of pictures and videos to the API.

- class `Version(object)` :

- class `VersionResource(ManticoreResource)` :

---

###  fields.py

- class `ToBareForeignKeyField(ToOneField)` :
Receives and Outputs ints representing primary keys of the field. Allows someone to pass just the ID for
    this field, which will in the overwritten method be converted into the proper resource_uri for the related object.


- class `BareGenericForeignKeyField(GenericForeignKeyField)` :
Same for generic foreign keys.