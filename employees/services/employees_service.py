from ..models.employees import Employees
from django.db import models

class EmployeeService:
    """
    Servicio para manejar la lógica de negocio de terapeutas
    """
    
    @staticmethod
    def search_employees(query):
        """Busca empleado por diferentes criterios"""
        return Employees.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(last_name_paternal__icontains=query) |
            models.Q(last_name_maternal__icontains=query) |
            models.Q(document_number__icontains=query) |
            models.Q(email__icontains=query),
            deleted_at__isnull=True
        )