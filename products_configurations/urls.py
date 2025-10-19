from django.urls import path
from .views.category import category_list, category_create, category_delete, category_edit, category_detail
from .views.supplier import supplier_list, supplier_create, supplier_delete, supplier_update, supplier_detail
urlpatterns = [
    # Category
    path("category/", category_list, name="category_list"),
    path("category/create/", category_create, name="category_create"),
    path("category/<int:pk>/edit/", category_edit, name="category_edit"),
    path("category/<int:pk>/delete/", category_delete, name="category_delete"),
    path("category/<int:pk>/", category_detail, name="category_detail"),

    # Proveedor
    path("supplier/", supplier_list, name="supplier_list"),
    path("supplier/create/", supplier_create, name="supplier_create"),
    path("supplier/<int:pk>/edit/", supplier_update, name="supplier_update"),
    path("supplier/<int:pk>/delete/", supplier_delete, name="supplier_delete"),
    path("supplier/<int:pk>/", supplier_detail, name="supplier_detail"),
]