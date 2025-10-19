from django.urls import path
from .views.employee import employee_list, employee_create, employee_delete, employee_update, employee_detail

urlpatterns = [
    # Rutas de histories
    path("employee/", employee_list, name="employee_list"),
    path("employee/create/", employee_create, name="employee_create"),
    path("employee/<int:pk>/", employee_detail, name="employee_detail"),
    path("employee/<int:pk>/edit/", employee_update, name="employee_update"),
    path("employee/<int:pk>/delete/", employee_delete, name="employee_delete"),
]