from rest_framework.permissions import BasePermission
from .models import AppUser


class IsPlacerUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == AppUser.UserType.PLACER
        )


class IsApproverUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == AppUser.UserType.APPROVER
        )
