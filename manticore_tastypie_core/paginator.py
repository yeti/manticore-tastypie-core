from django.utils.timezone import now
from tastypie.paginator import Paginator
from urllib import urlencode

__author__ = 'rudy'


class StreamPaginator(Paginator):
    """
    Paginates calls by putting a created date filter on the query if it
    doesn't exist so that duplicate objects are not sent down to the caller.
    Only works with resources with objects in descending order by `created`.

    A duplicate object will be sent down in the API when a new object has
    been created and increase the total count of this API call. By adding
    a `created` filter automatically we can avoid this from happening.
    """

    def get_previous(self, limit, offset):
        uri = super(StreamPaginator, self).get_previous(limit, offset)
        if uri and 'created' not in uri:
            uri += "&%s" % urlencode({'created__lte': now()})

        return uri

    def get_next(self, limit, offset, count):
        uri = super(StreamPaginator, self).get_next(limit, offset, count)
        if uri and 'created' not in uri:
            uri += "&%s" % urlencode({'created__lte': now()})

        return uri