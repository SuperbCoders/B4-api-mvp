from rest_framework import serializers

from filestorage.models import APIFile


class APIFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIFile
        read_only_fields = ('id', 'original_filename', 'ext', 'file_type', 'file_sub_type', 'file_duration', 'created_at')
        fields = ('id', 'file', 'original_filename', 'ext', 'file_type', 'file_sub_type', 'file_duration', 'created_at')
