from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.views import APIView

from app_run.models import Run, Status, AthleteInfo, Challenge, Position, CollectibleItem
from app_run.pagination import GeneralPagination
from app_run.serializers import RunSerializer, UsersSerializer, AthleteInfoSerializer, ChallengeSerializer, \
    PositionSerializer, CollectibleItemSerializer, FileUploadSerializer
from app_run.services.from_xlsx_to_model import import_xlsx_with_serializer
from app_run.services.run_service import start_run, stop_run

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
        try:
            run = start_run(run)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'status': run.status.label,
        })


class RunStoppedView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        try:
            run = stop_run(run)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'status': run.status.label,
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


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run']


class CollectibleItemViewSet(viewsets.ModelViewSet):
    queryset = CollectibleItem.objects.all()
    serializer_class = CollectibleItemSerializer


class UploadCollectibleItemsView(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer

    def get_queryset(self) -> None:
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            failed = import_xlsx_with_serializer(
                uploaded_file=uploaded_file,
                serializer_class=CollectibleItemSerializer,
                fields=['name', 'uid', 'value', 'latitude', 'longitude', 'picture'])
            return Response(failed, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
