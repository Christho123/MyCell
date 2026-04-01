from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.country import CountryViewSet
from .views.region import RegionViewSet
from .views.province import ProvinceViewSet
from .views.district import DistrictViewSet

router = DefaultRouter()
router.register(r"countries", CountryViewSet, basename="country")
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"provinces", ProvinceViewSet, basename="province")
router.register(r"districts", DistrictViewSet, basename="district")

urlpatterns = [
    path('', include(router.urls)),
]
