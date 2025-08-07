from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "confirmed_password"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
            password=validated_data["password"]
        )
        user.is_active = False
        user.save()
        return user
