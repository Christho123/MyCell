from django.urls import path
from .views.document_type import (
    DocumentTypePublicListView,
    DocumentTypePaginatedListView,
    document_type_all,
    document_type_create,
    document_type_delete,
    document_type_edit,
    document_type_detail,
)

urlpatterns = [
    path("document_type/all/", document_type_all, name="document_type_all"),
    path(
        "document_type/paginated/",
        DocumentTypePaginatedListView.as_view(),
        name="document_type_paginated",
    ),
    path("document_type/create/", document_type_create, name="document_type_create"),
    path("document_type/<int:pk>/edit/", document_type_edit, name="document_type_edit"),
    path("document_type/<int:pk>/delete/", document_type_delete, name="document_type_delete"),
    path("document_type/<int:pk>/", document_type_detail, name="document_type_detail"),
    path("document_type/", DocumentTypePublicListView.as_view(), name="document_type_public_list"),
]