from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import PatientReport, CustomUser
import logging

# Also How will createing superusers that can create say HR accounts work when I host since
# the db gets cleared?

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_groups(sender, **kwargs):  # called automatically after each migrating
    groups = [
        'Doctor', 'Clinician', 'Patient',
        'Registrar', 'Outreach Coordinator', 'Outreach Worker',
        'Public Health Analyst', 'Inventory Manager',
        'Finance Officer', 'Cashier', 'Hr', 'Receptionist'
    ]

    for group_name in groups:
        group, created = Group.objects.get_or_create(
            name=group_name
        )
        if created:
            logger.info(f"✅ Created group: {group_name}")
        else:
            logger.info(f"ℹ️ Group already exists: {group_name}")
    try:
        patient_report_ct = ContentType.objects.get_for_model(PatientReport)
        user_ct = ContentType.objects.get_for_model(CustomUser)

        doctors, _ = Group.objects.get_or_create(name='Doctor')
        doctors_perms, _ = Permission.objects.get_or_create(
            codename='can_view_all',
            name='Can view all patient reports',
            content_type=patient_report_ct
        )
        doctors.permissions.add(doctors_perms)

        hr, _ = Group.objects.get_or_create(name='Hr')
        hr_perms, _ = Permission.objects.get_or_create(
            codename='can_create_staff_account',
            name='Can create staff account',
            content_type=user_ct
        )
        hr.permissions.add(hr_perms)

        receptionist, _ = Group.objects.get_or_create(name='Receptionist')
        receptionist_perms, _ = Permission.objects.get_or_create(
            codename='can_create_patient_account',
            name='Can create patient account',
            content_type=user_ct
        )
        receptionist.permissions.add(receptionist_perms)
        logger.info("✅ Default permissions successfully linked to HR and Receptionist groups.")
    except Exception as e:
        logger.warning(f"⚠️ Could not assign permissions: {e}")

    logger.info("✅ Group setup complete after migrations.")
