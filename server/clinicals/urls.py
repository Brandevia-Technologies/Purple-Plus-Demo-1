from django.urls import path
from .views import CreatePatientRecordView, ViewPatientRecords, UpdatePatientRecordView

urlpatterns = [
    path(
        "patients/<int:patient_id>/records/create/",
        CreatePatientRecordView.as_view(),
        name="create-patient-record"
    ),
    path(
        "patients/<int:patient_id>/records/view/",
        ViewPatientRecords.as_view(),
        name="view-patient-record"
    ),
    path(
        "patients/<int:patient_id>/records/update/",
        UpdatePatientRecordView.as_view(),
        name="update-patient-record"
    )
]
