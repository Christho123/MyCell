from django.urls import path
from .views.document_type import document_type_list, document_type_create, document_type_delete, document_type_edit, document_type_detail

urlpatterns = [
    # Document Types
    path("document_type/", document_type_list, name="document_type_list"),
    path("document_type/create/", document_type_create, name="document_type_create"),
    path("document_type/<int:pk>/edit/", document_type_edit, name="document_type_edit"),
    path("document_type/<int:pk>/delete/", document_type_delete, name="document_type_delete"),
    path("document_type/<int:pk>/", document_type_detail, name="document_type_detail"),
]