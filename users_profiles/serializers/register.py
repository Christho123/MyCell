from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class PublicRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("user_name", "email", "document_number", "password", "password_confirm")

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                _("La contraseña debe tener al menos 8 caracteres.")
            )
        common_passwords = [
            "password",
            "123456",
            "12345678",
            "qwerty",
            "abc123",
            "password123",
            "admin",
            "letmein",
        ]
        if value.lower() in common_passwords:
            raise serializers.ValidationError(
                _("Esta contraseña es demasiado común. Elige una más segura.")
            )
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_("El correo es obligatorio."))
        if User.objects.filter(email__iexact=value.strip()).exists():
            raise serializers.ValidationError(_("Este correo ya está registrado."))
        return value.strip().lower()

    def validate_document_number(self, value):
        if not value:
            raise serializers.ValidationError(_("El número de documento es obligatorio."))
        if User.objects.filter(document_number=value).exists():
            raise serializers.ValidationError(_("Este número de documento ya está registrado."))
        return value

    def validate_user_name(self, value):
        if not value:
            raise serializers.ValidationError(_("El nombre de usuario es obligatorio."))
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError(_("Este nombre de usuario ya está registrado."))
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": _("Las contraseñas no coinciden.")}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user
