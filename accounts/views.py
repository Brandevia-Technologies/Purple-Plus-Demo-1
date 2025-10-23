from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .models import CustomUser, StaffProfile, PatientProfile
from django.contrib.auth.models import Group
from . import permissions
from .serializers import CustomUserSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


groups = [
        'Doctor', 'Clinician', 'Patient',
        'Registrar', 'Outreach Coordinator', 'Outreach Worker',
        'Public Health Analyst', 'Inventory Manager',
        'Finance Officer', 'Cashier', 'HR', 'Receptionist'
    ]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class StaffCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreateStaffAccounts]

    def perform_create(self, serializer):
        group_name = self.request.data.get("group")
        department = self.request.data.get("department")

        if not group_name:
            raise ValidationError({"group": "This field is required. Please specify a valid group name."})
        if group_name not in groups:
            raise ValidationError({
                "group": f"Group name should be in {', '.join(groups)} else it's invalid."
            })
        if not department:
            raise ValidationError({"department": "This field is required. "
                                                                   "Please specify a valid department name."})
        user = serializer.save(is_staff=True, is_patient=False)
        user.refresh_from_db()

        print("GROUP NAME", group_name)  #TODO: find a way to include this inside my serializer

        group, _ = Group.objects.get_or_create(name=group_name.strip().title())
        user.groups.add(group)

        staff_profile = getattr(user, "staff_profile", None)
        if staff_profile:
            staff_profile.department = department.strip()
            staff_profile.created_by = self.request.user

            staff_profile.save()
        else:
            # Fallback (if signal didn’t run for any reason)
            StaffProfile.objects.create(user=user, department=department.strip(), created_by=self.request.user)
        return user


class PatientsCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreatePatientAccounts]

    def perform_create(self, serializer):
        date_of_birth = self.request.data.get("dob")
        address = self.request.data.get("address")
        emergency_contact = self.request.data.get("emergency_contact")
        if not all([date_of_birth, address, emergency_contact]):
            raise ValidationError({"dob": "This field is required",
                                   "address": "This field is required",
                                   "emergency_contact": "This is a required field"})

        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            raise ValidationError({
                "dob": "Date must be in YYYY-MM-DD format"
            })

        user = serializer.save(is_patient=True, is_staff=False, )
        user.refresh_from_db()

        patient_profile = getattr(user, "patient_profile", None)
        if patient_profile:
            patient_profile.date_of_birth = date_of_birth
            patient_profile.address = address
            patient_profile.emergency_contact = emergency_contact
            patient_profile.created_by = self.request.user
            patient_profile.save()
        else:
            PatientProfile.objects.create(user=user, date_of_birth=date_of_birth,
                                        address=address, emergency_contact=emergency_contact, created_by=self.request.user)

        return user

