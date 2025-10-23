from django.urls import path
from .views import CustomTokenObtainPairView, StaffCreateView, PatientsCreateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('staff/create/', StaffCreateView.as_view(), name='create-staff'),
    path('patients/create/', PatientsCreateView.as_view(), name='create-patient')
]
