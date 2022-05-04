from rest_framework import serializers
import phonenumbers
from .models import User


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.CharField(default=None, allow_null=True)

    def validate_phone_number(self, obj):
        """
        Validate User Phone number
        """
        try:
            phone = "+" + str(int(obj)).replace(" ", "")
            x = phonenumbers.parse(phone, None)
        except Exception as e:
            raise serializers.ValidationError("Please enter a valid phone number")
        if not phonenumbers.is_valid_number(x):
            raise serializers.ValidationError(f"Invalid phone number {phone}")
        return obj


class UserSignInSerializer(serializers.Serializer):
    """
    Serializer

        - Email

        - Password
    """

    email = serializers.EmailField()
    password = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "created",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
