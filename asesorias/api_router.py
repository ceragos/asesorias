from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.ventas.api.views import clasificar, Balance
from apps.ventas.aplicacion.adapters.api.perfiles import PerfilAdapter

router = DefaultRouter()
# router.register(r'perfiles', PerfilViewSet)

app_name = "api"
urlpatterns = [
    path('clasificar/', clasificar, name='clasificar'),
    path('balance/', Balance.as_view(), name='balance'),
    path('perfiles/', PerfilAdapter.as_view(http_method_names=['get', 'post']), name='perfiles'),
    path('perfiles/<int:perfil_id>/', PerfilAdapter.as_view(http_method_names=['patch', 'delete']), name='perfiles'),
] + router.urls
