from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Run

user = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserInfoSerializer(source='athlete', read_only=True)
    # status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Run
        fields = ['id', 'athlete', 'created_at', 'comment', 'athlete_data', 'status']



class UsersSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        role_runner = {value: key for key, value in settings.RUNNER_ROLE.items()}
        return role_runner[obj.is_staff]
