# -*- coding: utf-8 -*-
from rest_framework.viewsets import ReadOnlyModelViewSet
from ubi_geo.models.province import Province
from ubi_geo.serializers.province import ProvinceSerializer
from .geo_paginated_mixin import PaginatedListActionMixin


class ProvinceViewSet(PaginatedListActionMixin, ReadOnlyModelViewSet):
    """
    GET /api/provinces/                 -> lista (se puede filtrar)
    GET /api/provinces/{id}/            -> detalle

    Filtros por querystring:
      - ?region=<id>            -> provincias de esa región
    """
    serializer_class = ProvinceSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Province.objects.select_related("region").filter(deleted_at__isnull=True).order_by("name")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs
