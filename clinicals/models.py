from django.db import models
from accounts.models import CustomUser

class PatientRecord(models.Model):
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ehr_records",
        limit_choices_to={"is_patient": True}
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_records",
        limit_choices_to={"is_staff": True}
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_records"
    )

    clinical_note = models.TextField()
    vitals = models.JSONField(default=dict, blank=True)
    allergies = models.JSONField(default=list, blank=True)
    immunizations = models.JSONField(default=list, blank=True)
    past_conditions = models.JSONField(default=list, blank=True)
    procedures = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_create_patient_record', 'Can create patient record'),
            ('can_view_patient_record', 'Can view patient record'),
            ('can_update_patient_record', 'Can update patient record'),
            ('can_delete_patient_record', 'Can delete patient record'),
        ]