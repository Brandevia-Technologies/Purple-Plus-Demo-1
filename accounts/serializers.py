from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, PatientProfile, StaffProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
        }
        return data


class PatientProfileSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'address', 'emergency_contact', 'created_by']


class StaffProfileSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    class Meta:
        model = StaffProfile
        fields = ['department', 'created_by']


class CustomUserSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer(required=False)
    staff_profile = StaffProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name','middle_name', 'last_name','sex',
                  'email', 'password', 'date_joined',
                  'last_login','patient_profile', 'staff_profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def create(self, validated_data):

        patient_profile_data = validated_data.pop('patient_profile', None)
        staff_profile_data = validated_data.pop('staff_profile', None)
        user = CustomUser.objects.create_user(**validated_data)
        if patient_profile_data:
            PatientProfile.objects.filter(user=user).update(**patient_profile_data)
        elif staff_profile_data:
            StaffProfile.objects.filter(user=user).update(**staff_profile_data)

        return user

