from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import PatientRecord
from accounts.models import PatientProfile
from .serializers import PatientRecordSerializer
from .permissions import CanViewPatientRecord, CanCreatePatientRecord

class CreatePatientRecordView(generics.CreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [CanCreatePatientRecord]
    queryset = PatientRecord.objects.none()

    def perform_create(self, serializer):
        patient = get_object_or_404(PatientProfile, user__id=self.kwargs['patient_id'])
        serializer.save(patient=patient.user, created_by=self.request.user)