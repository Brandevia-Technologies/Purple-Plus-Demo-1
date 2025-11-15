from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StaffProfile, PatientProfile

# gets called post-saving of customUser
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            StaffProfile.objects.create(user=instance)
        elif instance.is_patient:
            PatientProfile.objects.create(user=instance)
