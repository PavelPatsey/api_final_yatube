from rest_framework import permissions


class IsAuthorAndIsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
