from rest_framework.permissions import BasePermission

class CanCreatePatientRecord(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff and
                request.user.has_perm('clinicals.can_create_patient_record')
                and request.user.is_active)
class CanViewPatientRecord(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff and
                request.user.has_perm('clinicals.can_view_patient_record'))

class CanUpdatePatientRecord(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff and
                request.user.has_perm('clinicals.can_update_patient_record'))

class CanDeletePatientRecord(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff and
                request.user.has_perm('clinicals.can_delete_patient_record'))
