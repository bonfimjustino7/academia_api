from django.urls import path, include

urlpatterns = [
    path('', include('academia.urls')),
    path('', include('aluno.urls')),
    path('', include('auth_api.urls')),
    path('', include('matricula.urls')),
]