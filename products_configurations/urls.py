from django.urls import path
from .views.category import category_list, category_create, category_delete, category_edit, category_detail

urlpatterns = [
    # Category
    path("category/", category_list, name="category_list"),
    path("category/create/", category_create, name="category_create"),
    path("category/<int:pk>/edit/", category_edit, name="category_edit"),
    path("category/<int:pk>/delete/", category_delete, name="category_delete"),
    path("category/<int:pk>/", category_detail, name="category_detail"),
]