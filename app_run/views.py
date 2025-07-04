from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.views import APIView

from app_run.models import Run, Status, AthleteInfo, Challenge
from app_run.pagination import GeneralPagination
from app_run.serializers import RunSerializer, UsersSerializer, AthleteInfoSerializer, ChallengeSerializer

User = get_user_model()


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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = GeneralPagination


class GetUsersView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.annotate(
        runs_finished=Count('runs', filter=Q(runs__status=Status.FINISHED))
    )
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = GeneralPagination

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
                {"detail": 'Run cannot be started from the current status.'},
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
        if run.status != Status.IN_PROGRESS:
            return Response(
                {"detail": 'Run cannot be finished from the current status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = Status.FINISHED
        run.save()
        finished_runs = Run.objects.filter(athlete=run.athlete, status=Status.FINISHED).count()
        if finished_runs == 10:
            Challenge.objects.get_or_create(
                full_name='Сделай 10 Забегов!',
                athlete=run.athlete,
            )
        return Response({
            'status': Status.FINISHED.label,
        })


class AthleteInfoView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        athlete_info, _ = AthleteInfo.objects.get_or_create(user=user)

        serializer = AthleteInfoSerializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        athlete_info, _ = AthleteInfo.objects.get_or_create(user=user)

        serializer = AthleteInfoSerializer(instance=athlete_info, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetChallengesView(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.select_related('athlete').all()
    serializer_class = ChallengeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athlete']
