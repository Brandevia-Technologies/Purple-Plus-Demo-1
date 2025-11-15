from .globals import ALL_GROUPS
from django.db import transaction
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from .models import CustomUser, StaffProfile, PatientProfile
from django.contrib.auth.models import Group
from . import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model


# CREATE views
@api_view(["POST"])
@permission_classes([AllowAny])
def create_temp_superuser(request):
    User = get_user_model()

    if User.objects.filter(email="admin@gmail.com").exists():
        return Response({"status": "exists"})

    User.objects.create_superuser(
        email="admin@gmail.com",
        password="123admin123",
        first_name="Admin",
        middle_name="Admin",
        last_name="Admin",
        sex="Female",
    )

    return Response({"status": "created"})

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BaseUserCreateView(generics.CreateAPIView):
    profile_model = None  # override in subclass
    profile_fields = []  # list of profile fields to get from request.data

    def get_profile_data(self):
        """Helper to get profile data from request"""
        return {field: self.request.data.get(field) for field in self.profile_fields}

    def validate_required_fields(self, data):
        missing_or_empty = [f for f in self.profile_fields if not data.get(f)]
        if missing_or_empty:
            raise ValidationError({field: "This field is required." for field in missing_or_empty})

    def create(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                # Step 1: DRF standard validation (which includes unique email check)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                self.perform_create(serializer)

                # If all succeeds:
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except DRFValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({"success": False,
                             "detail": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def perform_create(self, serializer):
        # Save user first but inside atomic transaction
        user = serializer.save()
        user.refresh_from_db()

        # Gather profile data
        profile_data = self.get_profile_data()

        # Create or update profile
        profile = getattr(user, self.profile_model._meta.get_field('user').remote_field.related_name, None)
        try:
            if profile:
                # Update existing profile fields
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.created_by = self.request.user
                profile.full_clean()
                profile.save()
            else:
                self.profile_model.objects.create(user=user, created_by=self.request.user, **profile_data)

        except DjangoValidationError as e:
            # Raise DRF validation error, transaction will rollback automatically
            raise DRFValidationError(e.message_dict)

        return user


class StaffCreateView(BaseUserCreateView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreateStaffAccounts]

    profile_model = StaffProfile
    profile_fields = ['department', 'address', 'emergency_contact', 'nin']

    def perform_create(self, serializer):
        group_name = self.request.data.get("group")
        if not group_name:
            raise DRFValidationError({"group": "This field is required. Please specify a valid group name."})
        if group_name not in ALL_GROUPS:
            raise DRFValidationError({
                "group": f"Group name should be in {', '.join(ALL_GROUPS)} else it's invalid."
            })

        user = serializer.save(is_staff=True, is_patient=False)
        user.refresh_from_db()
        group, _ = Group.objects.get_or_create(name=group_name.strip().title())
        user.groups.add(group)

        # Call base perform_create for profile creation and validation inside transaction
        return super().perform_create(serializer)


class PatientsCreateView(BaseUserCreateView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.CanCreatePatientAccounts]

    profile_model = PatientProfile
    profile_fields = ['date_of_birth', 'address', 'emergency_contact', 'nin']

    def get_profile_data(self):
        """
        Override to map 'dob' from request.data to 'date_of_birth' in profile data.
        """
        data = super().get_profile_data()
        dob = self.request.data.get('dob')
        if dob:
            data['date_of_birth'] = dob
        return data

    def validate_required_fields(self, data):
        """
        Override to validate 'dob' existence and format separately since it comes
        under request.data key 'dob' not 'date_of_birth'.
        """
        dob = self.request.data.get('dob')
        if not dob:
            raise DRFValidationError({"dob": "This field is required."})

        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            raise DRFValidationError({"dob": "Date must be in YYYY-MM-DD format."})

        # Validate other profile fields normally
        super().validate_required_fields(data)

    def perform_create(self, serializer):
        user = serializer.save(is_patient=True, is_staff=False)
        user.refresh_from_db()

        return super().perform_create(serializer)

#READ views
class MeView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # This returns the currently authenticated user
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


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Use serializer to validate & save
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Password change failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "success": True,
            "detail": "Password updated successfully.",

        }, status=status.HTTP_200_OK)


#TODO: DELETE views


#LOGOUT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True, "detail": "Successfully logged out."},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"success": False, "detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



class BaseDeactivateView(generics.UpdateAPIView):
    def deactivate_user(self, user):
        if not user.is_active:
            return Response(
                {"success": False, "detail": "Account already deactivated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if self.request.user == user:
            return Response(
                {"success": False, "detail": "You cannot deactivate your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.is_superuser and self.request.user.is_superuser or not user.is_superuser:
            user.is_active = False
            user.save()
            return Response(
                {"success": True, "detail": "Account deactivated successfully."},
                status=status.HTTP_200_OK,
        )
        else:
            return Response(
                {"success": False, "detail": "You do not have permission to deactivate this user's account."},
                status=status.HTTP_403_FORBIDDEN,
            )

class DeactivatePatientAccountView(BaseDeactivateView):
    queryset = CustomUser.objects.filter(is_staff=False)
    permission_classes = [IsAuthenticated, permissions.CanCreatePatientAccounts]


class DeactivateStaffAccountView(BaseDeactivateView):
    queryset = CustomUser.objects.filter(is_staff=True)
    permission_classes = [IsAuthenticated, permissions.CanCreateStaffAccounts]
