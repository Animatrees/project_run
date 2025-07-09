from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_run.views import company_details_view, RunViewSet, GetUsersView, RunStartedView, RunStoppedView, \
    AthleteInfoView, GetChallengesView, PositionViewSet

router = DefaultRouter()
router.register('api/runs', RunViewSet)
router.register('api/users', GetUsersView)
router.register('api/challenges', GetChallengesView)
router.register('api/positions', PositionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details_view),
    path('api/runs/<int:run_id>/start/', RunStartedView.as_view(), name='run-started'),
    path('api/runs/<int:run_id>/stop/', RunStoppedView.as_view(), name='run-stopped'),
    path('api/athlete_info/<int:user_id>/', AthleteInfoView.as_view(), name='athlete_info'),
    path('', include(router.urls)),
]
