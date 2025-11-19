from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import PatientRecord
from accounts.models import PatientProfile
from .serializers import PatientRecordSerializer
from .permissions import CanCreatePatientRecord, PatientRecordPermission, CanViewPatientRecordList

class CreatePatientRecordView(generics.CreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [CanCreatePatientRecord]
    queryset = PatientRecord.objects.none()

    def perform_create(self, serializer):
        patient = get_object_or_404(PatientProfile, user__id=self.kwargs['patient_id'])
        serializer.save(patient=patient.user, created_by=self.request.user)


class ListPatientRecordsView(generics.ListAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [CanViewPatientRecordList]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientRecord.objects.filter(patient_id=patient_id)


class PatientRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [PatientRecordPermission]

    lookup_field = "id"
    lookup_url_kwarg = "record_id"

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        return PatientRecord.objects.filter(patient_id=patient_id)
