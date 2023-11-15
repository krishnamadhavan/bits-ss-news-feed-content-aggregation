from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
