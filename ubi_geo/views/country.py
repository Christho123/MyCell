from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ubi_geo.models.country import Country
from ubi_geo.serializers.country import CountrySerializer
from .geo_paginated_mixin import PaginatedListActionMixin


class CountryViewSet(PaginatedListActionMixin, ModelViewSet):
    queryset = Country.objects.filter(deleted_at__isnull=True).order_by("name")
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
