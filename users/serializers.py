from rest_framework.serializers import ModelSerializer
from users.models import Users
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(ModelSerializer):


    class Meta:
        model = Users
        fields = "__all__"


    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        same_password_sent = instance.check_password(password)
        if same_password_sent:
            raise serializers.ValidationError({"error": "try another password"})    
        else:
            instance.set_password(password)
            return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


