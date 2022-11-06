from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ModeratorPermission(permissions.BasePermission):
    pass


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return
        

class SuperUserPermission(permissions.BasePermission):
    pass
