from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, PatientProfile, StaffProfile, Profile
from django.contrib.auth import password_validation
from .validators import NINValidator


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
            'email': self.user.email,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
            'must_change_password': self.user.must_change_password
        }
        return data



class ProfileSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['created_by', 'address',
                  'emergency_contact', 'nin','created_at_formatted',]
        read_only_fields = ['created_by']
        extra_kwargs = {
            'nin': {
                'validators': [NINValidator()],
                'write_only': True
            },

        }
    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %B %Y")


class PatientProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        model = PatientProfile
        fields = ProfileSerializer.Meta.fields + ['date_of_birth']


class StaffProfileSerializer(ProfileSerializer):
        class Meta(ProfileSerializer.Meta):
            model = StaffProfile
            fields = ProfileSerializer.Meta.fields + ['department']



class CustomUserSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer(required=False)
    staff_profile = StaffProfileSerializer(required=False)

    group = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'sex',
                  'group', 'is_active', 'is_patient', 'is_staff', 'is_superuser',
                  'patient_profile', 'staff_profile', 'must_change_password']
        read_only_fields = ['date_joined', 'last_login',
                            'is_staff', 'is_superuser', 'is_active', 'is_patient']
        extra_kwargs = {
            'password': {'required': False, 'write_only': True},
        }

    def get_group(self, obj):
        group = obj.groups.first()
        return group.name if group else None

    def create(self, validated_data):
        """
        Create a CustomUser and attach related profile and group.
        DRF will pass extra kwargs from serializer.save(...) into this method.
        - validated_data: data validated by serializer (excludes nested profile dicts)
        - group (optional): group name to add the user to (string)
        - department (optional): department for staff_profile (string)
        - created_by (optional): user who performed creation (useful for StaffProfile.created_by)
        """
        # 1) Remove nested profile data from validated_data so we can call create_user()
        patient_profile_data = validated_data.pop('patient_profile', None)
        staff_profile_data = validated_data.pop('staff_profile', None)

        # 2) Create the user using manager's create_user (hashes password, sets defaults)
        #    This expects fields like email, password, first_name etc in validated_data.
        user = CustomUser.objects.create_user(**validated_data)
        if patient_profile_data:
            PatientProfile.objects.filter(user=user).update(**patient_profile_data)
        elif staff_profile_data:
            StaffProfile.objects.filter(user=user).update(**staff_profile_data)

        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_pw = serializers.CharField(write_only=True, required=True)
    new_pw = serializers.CharField(write_only=True, required=True)
    confirm_new_pw = serializers.CharField(write_only=True, required=True)

    def validate_old_pw(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old Password is incorrect')
        return value

    def validate_new_pw(self, value):
        password_validation.validate_password(value, self.context['request'].user)
        return value


    def validate(self, attrs):
        if attrs['new_pw'] != attrs['confirm_new_pw']:
            raise serializers.ValidationError({'confirm_new_pw': 'New passwords must match.'})
        if attrs['old_pw'] == attrs['new_pw']:
            raise serializers.ValidationError({'confirm_new_pw': 'New passwords cannot be the same as old password.'})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_pw'])
        user.must_change_password = False
        user.save()
        return user
