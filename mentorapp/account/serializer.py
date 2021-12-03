
from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Msg


#User = get_user_model()
# User serializer
# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password = validated_data['password'] ,first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Msg
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.sender = validated_data.get("sender", instance.sender)
        instance.receipient = validated_data.get("receipient", instance.receipient)
        instance.save()
        return instance
