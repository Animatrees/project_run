from .urls import urlpatterns  # импорт базовых маршрутов
import debug_toolbar
from django.urls import path, include

urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
]
