from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Run, AthleteInfo

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserInfoSerializer(source='athlete', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Run
        fields = ['id', 'athlete', 'created_at', 'comment', 'athlete_data', 'status']


class UsersSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        role_runner = {value: key for key, value in settings.RUNNER_ROLE.items()}
        return role_runner[obj.is_staff]

    def get_runs_finished(self, obj):
        return obj.runs_finished


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = AthleteInfo
        fields = ['weight', 'goals', 'user_id']

    def get_user_id(self, obj):
        return obj.user.id

    def validate_weight(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Вес должен быть больше 0.')

        if value is not None and value >= 900:
            raise serializers.ValidationError('Вес должен быть меньше 900.')

        return value
