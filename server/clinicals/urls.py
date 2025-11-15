from django.urls import path
from .views import CreatePatientRecordView

urlpatterns = [
    path(
        "patients/<int:patient_id>/records/create/",
        CreatePatientRecordView.as_view(),
        name="create-patient-record"
    ),
]
