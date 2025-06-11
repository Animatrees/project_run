from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.conf import settings

from app_run.models import Run
from app_run.serializers import RunSerializer, UsersSerializer

user = get_user_model()


@api_view(['GET'])
def company_details_view(request):
    return Response({
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS,
    })


class RunViewSet(viewsets.ModelViewSet):
    # queryset = Run.objects.select_related('athlete').all()
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class GetUsersView(viewsets.ReadOnlyModelViewSet):
    queryset = user.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)
        user_type = self.request.query_params.get('type', None)
        is_staff = settings.RUNNER_ROLE.get(user_type, None)

        if is_staff is not None:
            qs = qs.filter(is_staff=is_staff)

        return qs
