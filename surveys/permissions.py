
""" Permission helper functions for this app """

from django.core.exceptions import PermissionDenied

from .models import Survey


def affirm_survey_ownership(query):
    """
    Decorator to throw 403s if a user tries to access URIs under a survey they
    do not own.
    """
    def query_wrapper(obj, *args, **kwargs):
        """ The wrapped query """
        try:
            Survey.objects.get(id=obj.kwargs['sid'], owner=obj.request.user)
        except Survey.DoesNotExist:
            raise PermissionDenied
        return query(obj, *args, **kwargs)
    return query_wrapper
