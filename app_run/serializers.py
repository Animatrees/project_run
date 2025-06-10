from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Run

user = get_user_model()


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'athlete', 'created_at', 'comment']


class UsersSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        role_runner = {value: key for key, value in settings.RUNNER_ROLE.items()}
        return role_runner[obj.is_staff]
