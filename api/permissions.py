from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
        if request.method in SAFE_METHODS:
            return True

        # write methods: PUT/PATCH/DELETE
        return obj.owner == request.user
