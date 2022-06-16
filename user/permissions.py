from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsUserAdmin(BasePermission):

    def has_permission( self, request, view ):
        if request.user.is_admin:
            return True
        else:
            raise PermissionDenied('Permission Denied')


class IsInstanceOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        else:
            raise PermissionDenied('Permission Denied')

