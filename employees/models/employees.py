from django.db import models
from django.utils import timezone
from app_types.models.document_type import DocumentType
from ubi_geo.models import Region, Province, District
from architect.models.permission import Role

class Employees(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True, 
        null=True,
        verbose_name="Nombre"
    )

    last_name_paternal = models.CharField(
        max_length=150,
        blank=True, 
        null=True,
        verbose_name="Apellido Paterno"
    )

    last_name_maternal = models.CharField(
        max_length=150,
        blank=True, 
        null=True,
        verbose_name="Apellido Materno"
    )

    document_type = models.ForeignKey(
        DocumentType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Tipo de Documento")
    
    document_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        verbose_name="Número de documento"
    )

    email = models.EmailField(
        unique=True, 
        verbose_name="Correo electronico"
    )

    gender = models.CharField(
        max_length=1, 
        null=True, 
        blank=True, 
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        verbose_name="Sexo"
    )

    phone = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Telefono"
    )

    birth_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Fecha de nacimiento"
        )

    region = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE, 
        verbose_name="Región"
        )

    province = models.ForeignKey(
        Province, 
        on_delete=models.CASCADE, 
        verbose_name="Provincia")

    district = models.ForeignKey(
        District, 
        on_delete=models.CASCADE, 
        verbose_name="Distrito"
        )
        
    rol = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        verbose_name="Rol"
        )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, 
        null=True, 
        verbose_name="Salario"
        )
    
    photo = models.ImageField(
        upload_to='photo_employees/',
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Foto de perfil"
    )

    address = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Dirección"
        )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminacion")

    def __str__(self):
        return f"{self.name or ''} {self.last_name_paternal or ''} - {self.document_number or ''}"

    class Meta:
        db_table = "employees"
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['name', 'last_name_paternal', 'last_name_maternal']

    def get_full_name(self):
        return f"{self.name} {self.last_name_paternal} {self.last_name_maternal or ''}"

    def __str__(self):
        return self.get_full_name()

    def get_photo_url(self):
        if self.photo:
            return f"{settings.MEDIA_URL}{self.photo}"
        return None
