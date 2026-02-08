from rest_framework.permissions import BasePermission


def _get_user_from_request(request):
    return getattr(request, "user", None)

def _user_is_authenticated(user):
    return getattr(user, "is_authenticated", False)

class ProductPermissions(BasePermission):

    def has_permission(self, request, view):
        user = _get_user_from_request(request)

        if _user_is_authenticated(user):
            return False

        if request.method == "GET":
            return user.has_perm("app.user_order_view") or user.has_perm("app.admin_view")

        return user.has_perm("app.admin_view")

class OrderByUserPermissions(BasePermission):

    def has_permission(self, request, view):
        user = _get_user_from_request(request)

        if _user_is_authenticated(user):
            return False

        return user.has_perm("app.user_order_view")

class OrderByAdminPermissions(BasePermission):

    def has_permission(self, request, view):
        user = _get_user_from_request(request)

        if _user_is_authenticated(user):
            return False

        return user.has_perm("app.admin_view")