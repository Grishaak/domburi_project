from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     return bool((request.user and request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool((request.user and request.user.is_staff)
                    or (request.user and (obj.author == request.user)))
