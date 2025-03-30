from django.urls import path
from .views import buscar_operadora

urlpatterns = [
    path("buscar", buscar_operadora),
]
