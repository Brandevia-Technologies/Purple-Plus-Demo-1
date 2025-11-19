from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from clinicals.models import PatientRecord
from .globals import ALL_GROUPS
import logging


logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_groups(sender, **kwargs):  # called automatically after each migrating

    for group_name in ALL_GROUPS:
        group, created = Group.objects.get_or_create(
            name=group_name
        )
        if created:
            logger.info(f"✅ Created group: {group_name}")
        else:
            logger.info(f"ℹ️ Group already exists: {group_name}")
    try:
        patient_record_ct = ContentType.objects.get_for_model(PatientRecord)
        user_ct = ContentType.objects.get_for_model(CustomUser)

        doctors, _ = Group.objects.get_or_create(name='Doctor')
        nurses, _ = Group.objects.get_or_create(name='Nurse')
        # Patient record permissions
        create_PR, _ = view_PR, _ = Permission.objects.get_or_create(
            codename='can_create_patient_record',
            name='Can create patient record',
            content_type=patient_record_ct
        )

        view_PR, _ = Permission.objects.get_or_create(
            codename='can_view_patient_record',
            name='Can view patient record',
            content_type=patient_record_ct
        )
        update_PR, _ = Permission.objects.get_or_create(
            codename='can_update_patient_record',
            name='Can update patient record',
            content_type=patient_record_ct
        )
        delete_PR, _ = Permission.objects.get_or_create(
            codename='can_delete_patient_record',
            name='Can delete patient record',
            content_type=patient_record_ct
        )

        # permission to view a patient's profile
        doctors.permissions.add(create_PR, view_PR, update_PR, delete_PR)
        nurses.permissions.add(create_PR, view_PR, update_PR, delete_PR)

        hr, _ = Group.objects.get_or_create(name='Hr')
        create_staff, _ = Permission.objects.get_or_create(
            codename='can_create_staff_account',
            name='Can create staff account',
            content_type=user_ct
        )
        hr.permissions.add(create_staff)

        receptionist, _ = Group.objects.get_or_create(name='Receptionist')
        create_patient, _ = Permission.objects.get_or_create(
            codename='can_create_patient_account',
            name='Can create patient account',
            content_type=user_ct
        )
        receptionist.permissions.add(create_patient)
        logger.info("✅ Default permissions successfully linked to HR and Receptionist groups.")
    except Exception as e:
        logger.warning(f"⚠️ Could not assign permissions: {e}")

    logger.info("✅ Group setup complete after migrations.")
