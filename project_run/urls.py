from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_run.views import company_details_view, RunViewSet, GetUsersView, RunStartedView, RunStoppedView

router = DefaultRouter()
router.register('api/runs', RunViewSet)
router.register('api/users', GetUsersView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details_view),
    path('api/runs/<int:run_id>/start/', RunStartedView.as_view(), name='run-started'),
    path('api/runs/<int:run_id>/stop/', RunStoppedView.as_view(), name='run-stopped'),
    path('', include(router.urls)),
]
