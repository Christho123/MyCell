# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ubi_geo.models.district import District
from ubi_geo.serializers.district import DistrictSerializer
from .geo_paginated_mixin import PaginatedListActionMixin


class DistrictViewSet(PaginatedListActionMixin, ModelViewSet):
    """
    GET /api/locations/districts/         -> lista (se puede filtrar)
    GET /api/locations/districts/{id}/    -> detalle
    POST/PUT/PATCH/DELETE                 -> CRUD con JWT

    Filtros por querystring:
      - ?province=<id>           -> distritos de esa provincia
    """

    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = (
            District.objects
            .select_related("province", "province__region")
            .filter(deleted_at__isnull=True)
            .order_by("name")
        )
        province_id = self.request.query_params.get("province")
        if province_id:
            qs = qs.filter(province_id=province_id)
        return qs
