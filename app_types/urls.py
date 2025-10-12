from django.urls import path
from .views.document_type import document_type_list, document_type_create, document_type_delete, document_type_edit, document_type_detail
from .views.payment_type import payment_type_list, payment_type_create, payment_type_delete, payment_type_edit, payment_type_detail
from .views.payment_status import payment_status_list, payment_status_create, payment_status_edit, payment_status_delete, payment_status_detail

urlpatterns = [
    # Document Types
    path("document_type/", document_type_list, name="document_type_list"),
    path("document_type/create/", document_type_create, name="document_type_create"),
    path("document_type/<int:pk>/edit/", document_type_edit, name="document_type_edit"),
    path("document_type/<int:pk>/delete/", document_type_delete, name="document_type_delete"),
    path("document_type/<int:pk>/", document_type_detail, name="document_type_detail"),

    # Payment Types
    path("payment_type/", payment_type_list, name="payment_type_list"),
    path("payment_type/create/", payment_type_create, name="payment_type_create"),
    path('payment_type/<int:pk>/edit/', payment_type_edit, name='payment_type_edit'),
    path("payment_type/<int:pk>/delete/", payment_type_delete, name="payment_type_delete"),
    path("payment_type/<int:pk>/", payment_type_detail, name="payment_type_detail"),
    
    # Payment Status
    path("payment_status/", payment_status_list, name="payment_status_list"),
    path("payment_status/create/", payment_status_create, name="payment_status_create"),
    path('payment_status/<int:pk>/edit/', payment_status_edit, name='payment_status_edit'),
    path("payment_status/<int:pk>/delete/", payment_status_delete, name="payment_status_delete"),
    path("payment_status/<int:pk>/", payment_status_detail, name="payment_status_detail"),
]