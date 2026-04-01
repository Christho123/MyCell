from rest_framework import serializers
from ubi_geo.models.country import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "phone_code", "ISO2", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del país no puede estar vacío")
        return value.strip()
