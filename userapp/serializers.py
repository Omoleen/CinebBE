from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'confirmPassword', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({
                'password': 'passwords do not match',
                'confirmPassword': 'passwords do not match'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return self.Meta.model.objects.create_user(**validated_data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    token = serializers.CharField(max_length=128, read_only=True)

    class Meta:
        exclude = []


class VerifyTokenSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=256, write_only=True)
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        exclude = []
