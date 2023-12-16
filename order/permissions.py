# permissions.py
from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the order
        return obj.vendor == request.user
