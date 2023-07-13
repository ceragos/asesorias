from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.ventas.api.views import clasificar, Balance

router = DefaultRouter()

# router.register()

app_name = "api"
urlpatterns = [
    path('clasificar/', clasificar, name='clasificar'),
    path('balance/', Balance.as_view(), name='balance'),
] + router.urls