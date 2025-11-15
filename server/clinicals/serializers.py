from rest_framework import serializers
from .models import PatientRecord

class PatientRecordSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    patient = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = PatientRecord
        fields = '__all__'
        read_only_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']
    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %B %Y")