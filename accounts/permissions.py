from rest_framework.permissions import BasePermission


class CanViewAllReports(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_active

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('accounts.can_view_all')


class CanCreateStaffAccounts(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.has_perm('accounts.can_create_staff_account') and request.user.is_active


class CanCreatePatientAccounts(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.has_perm('accounts.can_create_patient_account') and request.user.is_active
