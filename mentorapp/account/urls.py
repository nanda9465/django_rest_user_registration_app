from django.conf.urls import url
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from .views import RegisterUsersView, MessageCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('api/docs', schema_view, name="docs"),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', RegisterUsersView.as_view(), name="auth-register"),
    path('api/login',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/create/message', MessageCreateView.as_view(), name="Message"),
]