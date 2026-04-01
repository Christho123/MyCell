# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ubi_geo.models.region import Region
from ubi_geo.serializers.region import RegionSerializer
from .geo_paginated_mixin import PaginatedListActionMixin


class RegionViewSet(PaginatedListActionMixin, ModelViewSet):
    """
    GET /api/locations/regions/           -> lista completa (sin paginar)
    GET /api/locations/regions/paginated/ -> paginado (10, 20, 50)
    GET /api/locations/regions/{id}/      -> detalle
    POST/PUT/PATCH/DELETE                 -> CRUD con JWT
    """

    queryset = Region.objects.filter(deleted_at__isnull=True).order_by("name")
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
