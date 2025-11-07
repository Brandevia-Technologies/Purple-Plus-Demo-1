from .globals import ALL_GROUPS
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from .models import CustomUser, StaffProfile, PatientProfile
from django.contrib.auth.models import Group
from . import permissions
from rest_framework.response import Response
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


# CREATE views
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
        if group_name not in ALL_GROUPS:
            raise ValidationError({
                "group": f"Group name should be in {', '.join(ALL_GROUPS)} else it's invalid."
            })
        if not department:
            raise ValidationError({"department": "This field is required. "
                                                 "Please specify a valid department name."})
        user = serializer.save(is_staff=True, is_patient=False)
        user.refresh_from_db()

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
                                          address=address, emergency_contact=emergency_contact,
                                          created_by=self.request.user)

        return user


#READ views
class MeView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # This returns the currently authenticated staff
        return self.request.user


class PatientListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser, permissions.CanCreatePatientAccounts]

    def get_queryset(self):
        all_patients = CustomUser.objects.filter(is_staff=False)

        # add the related profile and group to what gets returned
        return all_patients.select_related('patient_profile').prefetch_related('groups')


class PatientSearchView(generics.ListAPIView):
    """
    GET /api/patients/search/?email=... OR /api/patients/search/?q=...
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreatePatientAccounts, IsAdminUser]
    queryset = CustomUser.objects.filter(is_staff=False).select_related('patient_profile').prefetch_related('groups')

    def get_queryset(self):
        # base: active non-staff users (patients)
        qs = CustomUser.objects.filter(is_active=True, is_staff=False)

        # avoid N+1 when serializer reads related data
        qs = qs.select_related('patient_profile').prefetch_related('groups')

        # query params
        q = self.request.query_params.get('q').strip()  # generic search (email/name)
        email = self.request.query_params.get('email').strip()  # exact email search
        sex = self.request.query_params.get('sex').strip()  # sex (male/female)
        address = self.request.query_params.get('address').strip()  # patient_profile.address
        created_by = self.request.query_params.get('created_by').strip()  # creator email or id
        dob = self.request.query_params.get('dob').strip()

        # Generic search across fields (OR)
        if q:
            return qs.filter(
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(middle_name__icontains=q)
            )

        # Exact email filter (if provided)
        if email:
            qs = qs.filter(email__iexact=email)

        # Sex filter (exact, case-insensitive)
        if sex:
            qs = qs.filter(sex__iexact=sex)

        # Address filter on the related PatientProfile (substring search)
        if address:
            qs = qs.filter(patient_profile__address__icontains=address)

        # created_by filter
        if created_by:
            qs = qs.filter(patient_profile__created_by__email__iexact=created_by)
        # date of birth filter (substring search: so users can search by year or day)
        if dob:
            qs = qs.filter(patient_profile__date_of_birth__icontains=dob)

        return qs


class StaffListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser, permissions.CanCreateStaffAccounts]

    def get_queryset(self):
        all_staff = CustomUser.objects.filter(is_staff=True)

        # add the related profile and group to what gets returned
        return all_staff.select_related('staff_profile').prefetch_related('groups')


class StaffSearchView(generics.ListAPIView):
    """
    GET /api/patients/search/?email=... OR /api/patients/search/?q=...
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreateStaffAccounts, IsAdminUser]
    queryset = CustomUser.objects.filter(is_staff=True).select_related('staff_profile').prefetch_related('groups')

    def get_queryset(self):
        # base: active non-staff users (patients)
        qs = CustomUser.objects.filter(is_active=True, is_staff=True)

        # avoid N+1 when serializer reads related data
        qs = qs.select_related('staff_profile').prefetch_related('groups')

        # query params
        q = self.request.query_params.get('q', '').strip()  # generic search (email/name)
        email = self.request.query_params.get('email', '').strip()  # exact email search
        sex = self.request.query_params.get('sex', '').strip()  # sex (male/female)
        created_by = self.request.query_params.get('created_by', '').strip()  # creator email or id
        department = self.request.query_params.get('department', '').strip()
        group = self.request.query_params.get('group', '').strip()

        # Generic search across fields (OR)
        if q:
            return qs.filter(
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(middle_name__icontains=q)
            )

        # Exact email filter (if provided)
        if email:
            qs = qs.filter(email__iexact=email)

        # Sex filter (exact, case-insensitive)
        if sex:
            qs = qs.filter(sex__iexact=sex)

        # created_by filter
        if created_by:
            qs = qs.filter(staff_profile__created_by__email__iexact=created_by)

        if department:
            qs = qs.filter(staff_profile__department__iexact=department)
        if group:
            qs = qs.filter(groups__name__iexact=group)
        qs = qs.distinct()

        return qs

# TODO: UPDATE views
class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Use serializer to validate & save
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

#TODO: DELETE views


#LOGOUT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
