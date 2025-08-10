from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        else:
            return False

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False