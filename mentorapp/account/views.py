from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializer import UserSerializer, RegisterSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.generic import CreateView
from .models import Msg
from .decorators import validate_request_data
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class RegisterUsersView(generics.CreateAPIView):
    """
    POST authentication/register/
    """
    permission_classes = (AllowAny,)

    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class MessageCreateView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = User.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        user = User.objects.get(email = request.data["sender"])
        print(user)
        msg = Msg.objects.create(
            sender=user.email,
            receipient=user
        )
        return Response(
            data=MessageSerializer(msg).data,
            status=status.HTTP_201_CREATED
        )


