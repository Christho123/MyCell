from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company_reports.views.company_views import CompanyDataViewSet


router = DefaultRouter()
router.register(r'company', CompanyDataViewSet, basename='company')

# Agrupar rutas por funcionalidad
api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = []
urlpatterns.extend(api_urlpatterns)