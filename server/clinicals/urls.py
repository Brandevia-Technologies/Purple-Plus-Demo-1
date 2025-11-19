from django.urls import path
from .views import CreatePatientRecordView, ListPatientRecordsView, PatientRecordDetailView

urlpatterns = [
    path(
        "patients/<int:patient_id>/records/create/",
        CreatePatientRecordView.as_view(),
        name="create-patient-record"
    ),
    path(
        "patients/<int:patient_id>/records/view/",
        ListPatientRecordsView.as_view(),
        name="view-patient-record"
    ),
    path(
        "patients/<int:patient_id>/records/<int:record_id>/",
        PatientRecordDetailView.as_view(),
        name="patient-record-detail"
    ),
]
