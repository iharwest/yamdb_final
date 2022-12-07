from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAuthenticatedOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
