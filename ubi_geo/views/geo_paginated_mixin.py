from rest_framework.decorators import action

from pagination import AllowedSizesPageNumberPagination


class PaginatedListActionMixin:
    """Añade GET .../paginated/ con page_size en {10, 20, 50}."""

    @action(detail=False, url_path="paginated", methods=["get"])
    def paginated(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = AllowedSizesPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
