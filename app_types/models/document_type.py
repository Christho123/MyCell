from django.db import models
from django.utils import timezone

class DocumentType(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True, 
        null=True,
        verbose_name="Nombre"
    )
    
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminacion")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "document_types"
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
        ordering = ['name']
