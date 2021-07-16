from django.urls import path

from .api.viewsets import AuthToken

urlpatterns = [
    path('auth/', AuthToken.as_view())
]