# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ubi_geo.models.province import Province
from ubi_geo.serializers.province import ProvinceSerializer
from .geo_paginated_mixin import PaginatedListActionMixin


class ProvinceViewSet(PaginatedListActionMixin, ModelViewSet):
    """
    GET /api/locations/provinces/         -> lista (se puede filtrar)
    GET /api/locations/provinces/{id}/    -> detalle
    POST/PUT/PATCH/DELETE                 -> CRUD con JWT

    Filtros por querystring:
      - ?region=<id>            -> provincias de esa región
    """

    serializer_class = ProvinceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = Province.objects.select_related("region").filter(deleted_at__isnull=True).order_by("name")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs
