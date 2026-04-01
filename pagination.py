"""Paginación reutilizable: page_size solo 10, 20 o 50 (query ?page_size=)."""
from rest_framework.pagination import PageNumberPagination


class AllowedSizesPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    ALLOWED = frozenset({10, 20, 50})

    def get_page_size(self, request):
        if request is None:
            return self.page_size
        raw = request.query_params.get(self.page_size_query_param)
        if raw is None:
            return self.page_size
        try:
            n = int(raw)
        except (TypeError, ValueError):
            return self.page_size
        return n if n in self.ALLOWED else self.page_size


def paginate_queryset(request, queryset, map_obj, pagination_class=None):
    """
    Pagina un queryset y devuelve Response DRF con results (listas de dicts/obj serializados).
    """
    cls = pagination_class or AllowedSizesPageNumberPagination
    paginator = cls()
    page = paginator.paginate_queryset(queryset, request)
    data = [map_obj(obj) for obj in page]
    return paginator.get_paginated_response(data)
