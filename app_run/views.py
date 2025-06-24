from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.views import APIView

from app_run.models import Run, Status
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
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer


class GetUsersView(viewsets.ReadOnlyModelViewSet):
    queryset = user.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)
        user_type = self.request.query_params.get('type', None)
        is_staff = settings.RUNNER_ROLE.get(user_type, None)

        if is_staff is not None:
            qs = qs.filter(is_staff=is_staff)

        return qs


class RunStartedView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status != Status.INIT:
            return Response(
                {"detail": "Run cannot be started from the current status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = Status.IN_PROGRESS
        run.save()
        return Response({
            'status': Status.IN_PROGRESS.label,
        })


class RunStoppedView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        # if run.status != Status.IN_PROGRESS:
        #     return Response(
        #         {"detail": "Run cannot be finished from the current status."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        if run.status == Status.INIT:
            return Response(
                        {"detail": "Run must be started in order to finish it."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        run.status = Status.FINISHED
        run.save()
        return Response({
            'status': Status.FINISHED.label,
        })
