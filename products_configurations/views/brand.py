import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.brand import Brand

@csrf_exempt
def brand_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    qs = Brand.objects.select_related("country")
    data = []
    for b in qs:
        data.append({
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "country": (
                {"id": b.country_id, "name": b.country.name}
                if b.country else None
            ),
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "updated_at": b.updated_at.isoformat() if b.updated_at else None
        })
    return JsonResponse({"brands": data})

@csrf_exempt
def brand_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Manejo de JSON inválido
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)

    country_id = payload.get("country")

    # Validar campos obligatorios
    if country_id is None:
        return JsonResponse({"error": "Campos obligatorios faltantes: country"}, status=400)

    try:
        # Preparar datos para crear el historial
        brand_data = {
            'name': payload.get("name"),
            'description': payload.get('description'),
            'country_id': country_id,
        }

        # Filtrar valores None para campos opcionales
        filtered_data = {k: v for k, v in brand_data.items() if v is not None}

        b = Brand.objects.create(**filtered_data)

        # Preparar respuesta con todos los campos del historial creado
        response_data = {
            "message": "Marca creada exitosamente",
            "brand": {
                "id": b.id,
                "name": b.name,
                "description": b.description,
                "country": (
                    {"id": b.country_id, "name": b.country.name}
                    if b.country else None
                ),
                "created_at": b.created_at.isoformat() if b.created_at else None,
                "updated_at": b.updated_at.isoformat() if b.updated_at else None
            }
        }

        return JsonResponse(response_data, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error al crear la marca: {str(e)}"}, status=500)

@csrf_exempt
def brand_update(request, pk):
    """
    Endpoint PUT para actualizar una marca existente
    """
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])

    try:
        # Buscar el historial activo
        brand = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return JsonResponse({"error": "Marca no encontrada o eliminada"}, status=404)

    # Manejo de JSON inválido
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)

    # Campos permitidos para actualización
    allowed_fields = {
        'name': 'name',
        'description': 'description',
        'country': 'country_id',
    }

    try:
        with transaction.atomic():
            # Actualizar campos permitidos
            for field_name, model_field in allowed_fields.items():
                if field_name in payload:
                    value = payload[field_name]
                    setattr(brand, model_field, value)
            
            # Guardar los cambios
            brand.save()
            
            # Preparar respuesta con datos actualizados
            updated_data = {
                "id": brand.id,
                "name": brand.name,
                "description": brand.description,
                "country": (
                    {"id": brand.country_id, "name": brand.country.name}
                    if brand.country else None
                ),
                "updated_at": brand.updated_at.isoformat() if brand.updated_at else None
            }
            
            return JsonResponse({
                "message": "Marca actualizada exitosamente",
                "brand": updated_data
            }, status=200)
            
    except Exception as e:
        return JsonResponse({"error": f"Error al actualizar la marca: {str(e)}"}, status=500)

@csrf_exempt
def brand_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    
    try:
        b = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    
    b.delete()
    return JsonResponse({"status": "deleted"})

@csrf_exempt
def brand_detail(request, pk):
    """
    GET - Obtener marca específica
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    try:
        brand = Brand.objects.select_related("country").get(pk=pk)
        data = {
            "id": brand.id,
            "name": brand.name,
            "description": brand.description,
            "country": (
                {"id": brand.country_id, "name": brand.country.name}
                if brand.country else None
            ),
            "created_at": brand.created_at.isoformat() if brand.created_at else None,
            "updated_at": brand.updated_at.isoformat() if brand.updated_at else None
        }
        return JsonResponse(data)
    except Brand.DoesNotExist:
        return JsonResponse({"error": "Marca no encontrada"}, status=404)