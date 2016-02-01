
from surveys.models import Survey

from django.core.exceptions import PermissionDenied
from rest_framework import permissions


def affirm_survey_ownership(query):
    """
    Given a query for a specific survey from a specific survey, check that 
    the user is the owner of said survey. If not, raise a 403 (forbidden).
    """
    def query_wrapper(obj):
        try:
            Survey.objects.get(id=obj.kwargs['sid'], owner=obj.request.user)
        except Survey.DoesNotExist:
            raise PermissionDenied
        query(obj)
    return query_wrapper


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a survey to edit it
    """

    def has_object_permission(self, request, view, obj):
        # Write and read permissions are only given to the owner of the survey.
        return obj.owner == request.user

