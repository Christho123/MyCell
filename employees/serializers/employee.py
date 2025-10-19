from rest_framework import serializers
from ..models import Employees
import re
from datetime import date
from app_types.models import DocumentType

class EmployeeSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Employees
        fields = [
            'id', 'document_type', 'document_type_id', 'rol', 'rol_id',
            'name', 'last_name_paternal', 'last_name_maternal', 'document_number',
            'email', 'gender', 'phone', 'birth_date', 'region', 'region_id', 'province',
            'province_id', 'district', 'district_id', 'salary', 'address', 'full_name', 
            'photo_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        """
        Asegura coherencia jerárquica:
        province debe pertenecer a region
        district debe pertenecer a province
        """
        region = attrs.get("region") or getattr(self.instance, "region", None)
        province = attrs.get("province") or getattr(self.instance, "province", None)
        district = attrs.get("district") or getattr(self.instance, "district", None)

        if province and region and province.region_id != region.id:
            raise serializers.ValidationError(
                "La provincia seleccionada no pertenece a la región."
            )
        if district and province and district.province_id != province.id:
            raise serializers.ValidationError(
                "El distrito seleccionado no pertenece a la provincia."
            )
        return attrs
    
    def validate_document_number(self, value):
        # Obtener el tipo de documento desde los datos iniciales o la instancia
        doc_type_id = self.initial_data.get("document_type_id")
        
        # Si no está en initial_data, intentar obtener de la instancia existente
        if not doc_type_id and self.instance:
            doc_type_id = self.instance.document_type_id
        
        if not doc_type_id:
            return value  # No podemos validar sin tipo de documento
        
        # Obtener el nombre del tipo de documento para las validaciones
        try:
            document_type = DocumentType.objects.get(id=doc_type_id)
            doc_type_name = document_type.name.upper()
        except DocumentType.DoesNotExist:
            # La validación de existencia se hará en document_type_id field
            return value

        # Validaciones según el tipo de documento
        if doc_type_name == "DNI":
            if not value.isdigit():
                raise serializers.ValidationError("El DNI debe contener solo números.")
            if not (8 <= len(value) <= 9):
                raise serializers.ValidationError(
                    "El DNI debe tener entre 8 y 9 dígitos."
                )

        elif doc_type_name == "CE" or "CARNE DE EXTRANJERIA" in doc_type_name:
            if not value.isdigit():
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe contener solo números."
                )
            if len(value) > 12:
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe tener máximo 12 dígitos."
                )

        elif doc_type_name == "PTP":
            if not value.isdigit():
                raise serializers.ValidationError("El PTP debe contener solo números.")
            if len(value) != 9:
                raise serializers.ValidationError(
                    "El PTP debe tener exactamente 9 dígitos."
                )

        elif doc_type_name == "CR" or "CARNE DE REFUGIADO" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Carné de Refugiado debe contener solo letras y números."
                )

        elif doc_type_name == "PAS" or "PASAPORTE" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Pasaporte debe contener solo letras y números."
                )

        return value
    
    def validate_birth_date(self, value):
        if value:
            today = date.today()

            # No permitir fechas futuras
            if value.date() > today:
                raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")

            # Calcular edad
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise serializers.ValidationError("El terapeuta debe tener al menos 18 años.")

        return value
        
    def get_full_name(self, obj):
        """Concatena name + last_name_paternal + last_name_maternal"""
        full_name_parts = []
        
        if obj.name:
            full_name_parts.append(obj.name)
        if obj.last_name_paternal:
            full_name_parts.append(obj.last_name_paternal)
        if obj.last_name_maternal:
            full_name_parts.append(obj.last_name_maternal)
            
        return ' '.join(full_name_parts) if full_name_parts else ''

    def get_photo_url(self, obj):
        """Retorna la URL de la foto del empleado"""
        return obj.get_photo_url()
