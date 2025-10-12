from django.db import models
from django.utils import timezone

class PaymentStatus(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        verbose_name="Nombre"
    )

    description = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'payment_status'
        verbose_name = "Estado de pago"
        verbose_name_plural = "Estados de pago"
        ordering = ['name']