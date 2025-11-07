from django.urls import path
from .views import (CustomTokenObtainPairView,
                    StaffCreateView, PatientsCreateView, MeView,
                    PatientListView, PatientSearchView, StaffListView,
                    StaffSearchView, PasswordChangeView, LogoutView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('staff/create/', StaffCreateView.as_view(), name='create-staff'),
    path('patients/create/', PatientsCreateView.as_view(), name='create-patient'),
    path('me/', MeView.as_view(), name='view-profile'),
    path('all/patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/search/', PatientSearchView.as_view(), name='patient-search'),
    path('all/staff/', StaffListView.as_view(), name='patient-list'),
    path('staff/search/', StaffSearchView.as_view(), name='patient-search'),
    path('change/password/', PasswordChangeView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
