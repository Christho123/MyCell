from django.contrib import admin
from .models.payment_type import PaymentType
from .models.document_type import DocumentType
from .models.payment_status import PaymentStatus

#Registrar el modelo en el admin
@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['id', 'name', 'description']
