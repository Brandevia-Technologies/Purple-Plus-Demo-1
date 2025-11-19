from rest_framework.permissions import BasePermission, SAFE_METHODS

class CanCreatePatientRecord(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff and
                request.user.has_perm('clinicals.can_create_patient_record')
                and request.user.is_active)

class CanViewPatientRecordList(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        patient_id = view.kwargs.get("patient_id")
        if not user.is_authenticated:
            return False
        # Staff with permission
        if user.is_staff and user.has_perm("clinicals.can_view_patient_record"):
            return True
        # Patient can only view their own records (compare ids)
        if hasattr(user, "is_patient") and user.is_patient and str(user.id) == str(patient_id):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated and user.is_staff and user.has_perm("clinicals.can_view_patient_record"):
            return True

        if user.is_authenticated and user.id == obj.patient_id:
            return True

        return False
class PatientRecordPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated and hasattr(user, "is_patient") and user.is_patient:
            if request.method in SAFE_METHODS:
                return obj.patient_id == user.id
            return False

        if user.is_authenticated and user.is_staff:
            if request.method in SAFE_METHODS:  # GET / HEAD / OPTIONS
                return user.has_perm("clinicals.can_view_patient_record")

            if request.method in ("PUT", "PATCH"):
                return user.has_perm("clinicals.can_update_patient_record")

            if request.method == "DELETE":
                return user.has_perm("clinicals.can_delete_patient_record")

        return False