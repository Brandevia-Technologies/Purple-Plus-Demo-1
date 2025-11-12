from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from .validators import NINValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, sex, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First name is required")
        if not middle_name:
            raise ValueError("Middle name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if password is None or password == '':  # password is email address without the @ until changed by the user
            password = email.split('@')[0]
            extra_fields["must_change_password"] = True
        if not sex:
            raise ValueError("Sex is required")
        if sex.lower() not in ['female', 'male']:
            raise ValidationError("Sex should be filled in as assigned at birth.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            first_name=first_name, middle_name=middle_name, last_name=last_name,
            sex=sex, email=email, **extra_fields
        )
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not password:
            raise ValueError("Superuser must have a password")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    sex = models.CharField(
        max_length=6,
        choices=[('Male', 'Male'), ('Female', 'Female')],
    )

    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', 'sex']

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ('can_create_staff_account', 'Can create staff account'),
            ('can_create_patient_account', 'Can create patient account'),
        ]

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    def clean(self):
        super().clean()
        """Ensure exactly one of is_staff or is_patient is True."""
        if not (self.is_staff or self.is_patient):
            raise ValidationError("User must be either staff or patient.")
        if self.is_staff and self.is_patient:
            raise ValidationError("User cannot be both staff and patient.")

    def save(self, *args, **kwargs):
        self.full_clean()  # runs the clean() validation before saving
        super().save(*args, **kwargs)

class Profile(models.Model):
    nin = models.CharField(max_length=11, validators=[NINValidator()])
    address = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Profile (NIN: {self.nin})"


class StaffProfile(Profile):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    department = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_created'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"


class PatientProfile(Profile):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_created'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - Patient"

class PatientReport(models.Model):
    report = models.CharField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_report')

    class Meta:
        permissions = [
            ("can_update", "Can update patient report"),
            ("can_view", 'Can view single patient reports'),
            ("can_view_all", "Can view all patient reports"),
            ("can_delete", "Can delete patient report"),
        ]
