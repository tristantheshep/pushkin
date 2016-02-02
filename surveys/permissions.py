
from surveys.models import Survey

from django.core.exceptions import PermissionDenied
from rest_framework import permissions


def affirm_survey_ownership(query):
    """
    Decorator to throw 403s if a user tries to access URIs under a survey they
    do not own.
    """
    def query_wrapper(obj, *args, **kwargs):
        try:
            Survey.objects.get(id=obj.kwargs['sid'], owner=obj.request.user)
        except Survey.DoesNotExist:
            raise PermissionDenied
        return query(obj, *args, **kwargs)
    return query_wrapper


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a survey to edit it
    """

    def has_object_permission(self, request, view, obj):
        # Write and read permissions are only given to the owner of the survey.
        return obj.owner == request.user

