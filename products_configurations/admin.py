from django.contrib import admin
from .models.category import Category
from .models.supplier import Supplier

#Registrar el modelo en el admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

#Registrar el modelo en el admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruc','company_name', 'business_name', 'representative', 'phone',
            'email', 'address', 'account_number', 'region', 'province', 'district')
    search_fields = ('ruc', 'company_name', 'business_name', 'representative')
    ordering = ('company_name', 'ruc', 'representative', 'business_name')
    readonly_fields = ('created_at', 'updated_at')