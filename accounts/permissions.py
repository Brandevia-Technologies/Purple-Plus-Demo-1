from rest_framework.permissions import BasePermission

class CanCreateStaffAccounts(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.has_perm('accounts.can_create_staff_account') and request.user.is_active


class CanCreatePatientAccounts(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.has_perm('accounts.can_create_patient_account') and request.user.is_active