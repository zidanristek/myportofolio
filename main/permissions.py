from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Anyone reads. Only the superuser writes, which is the rule the HTML
    pages already follow. IsAdminUser would check is_staff instead."""

    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Editors may correct an existing experience but never create or delete one.

    The Editor group grants change_experience (migration 0009), and the HTML
    edit page already checks that permission, so the API checks the same one
    instead of the group name.
    """

    message = "Only the portfolio owner or an editor can change experiences."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.has_perm("main.change_experience")
        )
