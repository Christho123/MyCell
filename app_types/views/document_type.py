import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from pagination import AllowedSizesPageNumberPagination

from ..models.document_type import DocumentType
from ..serializers.document_type import DocumentTypeSerializer
from ..services import document_type_service as service


def _json_body(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}


class DocumentTypePublicListView(generics.ListAPIView):
    """GET /document_type/ — público, paginado (page_size: 10, 20, 50)."""

    serializer_class = DocumentTypeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = AllowedSizesPageNumberPagination

    def get_queryset(self):
        return DocumentType.objects.filter(deleted_at__isnull=True).order_by("name")


class DocumentTypePaginatedListView(generics.ListAPIView):
    """GET /document_type/paginated/ — JWT, paginado (10, 20, 50)."""

    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    pagination_class = AllowedSizesPageNumberPagination

    def get_queryset(self):
        return DocumentType.objects.filter(deleted_at__isnull=True).order_by("-created_at", "-id")


@csrf_exempt
@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def document_type_all(request):
    """GET /document_type/all/ — JWT, lista completa sin paginar."""
    items = service.list_active()
    data = DocumentTypeSerializer(items, many=True).data
    return JsonResponse({"document_type": data})


@csrf_exempt
@api_view(["POST"])
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def document_type_create(request):
    payload = _json_body(request)
    serializer = DocumentTypeSerializer(data=payload)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    obj = service.create(**serializer.validated_data)
    return JsonResponse(DocumentTypeSerializer(obj).data, status=201)


@csrf_exempt
@api_view(["PUT", "PATCH"])
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def document_type_edit(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)

    payload = _json_body(request)
    serializer = DocumentTypeSerializer(obj, data=payload, partial=True)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    obj = service.update(obj, **serializer.validated_data)
    return JsonResponse(DocumentTypeSerializer(obj).data, status=200)


@csrf_exempt
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def document_type_delete(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)
    service.soft_delete(obj)
    return JsonResponse({"status": "deleted", "id": pk}, status=200)


@csrf_exempt
@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def document_type_detail(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)
    return JsonResponse(DocumentTypeSerializer(obj).data, status=200)
