import json
import os
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..models.supplier import Supplier
from datetime import datetime

@csrf_exempt
def supplier_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = Supplier.objects.select_related("region", "province", "district")
    data = []
    for s in qs:
        data.append({
            "id": s.id,
            "ruc": s.ruc,
            "company_name": s.company_name,
            "business_name": s.business_name,
            "representative": s.representative,
            "phone": s.phone,
            "email": s.email,
            "address": s.address,
            "account_number": s.account_number,
            "region": (
                {"id": s.region.id, "name": s.region.name}
                if s.region else None
            ),
            "province": (
                {"id": s.province.id, "name": s.province.name}
                if s.province else None
            ),
            "district": (
                {"id": s.district.id, "name": s.district.name}
                if s.district else None
            ),
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None
        })
    return JsonResponse({"suppliers": data})


@csrf_exempt
def supplier_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)

    try:
        # Preparar datos para el serializer
        supplier_data = {
            "ruc": payload.get('ruc'),
            "company_name": payload.get('company_name'),
            "business_name": payload.get('business_name'),
            "representative": payload.get('representative'),
            "phone": payload.get('phone'),
            "email": payload.get('email'),
            "address": payload.get('address'),
            "account_number": payload.get('account_number'),
            'region_id': payload.get('region'),
            'province_id': payload.get('province'),
            'district_id': payload.get('district'),
        }

        # Usar el serializer para validar y crear
        from ..serializers.supplier import SupplierSerializer
        serializer = SupplierSerializer(data=supplier_data)
        
        if serializer.is_valid():
            supplier = serializer.save()
            
            # Respuesta usando el serializer para obtener el formato correcto
            response_data = {
                "message": "Proveedor creado exitosamente",
                "supplier": serializer.data
            }
            
            return JsonResponse(response_data, status=201)
        else:
            # Devolver errores de validación
            return JsonResponse({"errors": serializer.errors}, status=400)
            
    except Exception as e:
        return JsonResponse({"error": f"Error al crear al proveedor: {str(e)}"}, status=500)


@csrf_exempt
def supplier_update(request, pk):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponseNotAllowed(["PUT", "PATCH"])
    
    # Buscar proveedor
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return JsonResponse({"error": "Proveedor no encontrado"}, status=404)
    
    # Leer JSON
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)
    
    # Preparar datos para el serializer
    supplier_data = {}
    field_mapping = {
        'ruc': 'ruc',
        'company_name': 'company_name',
        'business_name': 'business_name',
        'representative': 'representative',
        'phone': 'phone',
        'email': 'email',
        'address': 'address',
        'account_number': 'account_number',
        'region': 'region_id',
        'province': 'province_id',
        'district': 'district_id',
    }
    
    for payload_field, model_field in field_mapping.items():
        if payload_field in payload:
            supplier_data[model_field] = payload[payload_field]
    
    # Usar el serializer para validar y actualizar
    from ..serializers.supplier import SupplierSerializer
    serializer = SupplierSerializer(supplier, data=supplier_data, partial=True)
    
    if serializer.is_valid():
        updated_supplier = serializer.save()
        
        response_data = {
            "message": "Proveedor actualizado exitosamente",
            "supplier": serializer.data
        }
        
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({"errors": serializer.errors}, status=400)


@csrf_exempt
def supplier_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    
    try:
        s = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    s.delete()
    return JsonResponse({"message": "Proveedor eliminado exitosamente",
                         "status": "deleted",
                         "supplier_id": pk})


@csrf_exempt
def supplier_detail(request, pk):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    try:
        supplier = Supplier.objects.select_related("region", "province", "district").get(pk=pk)
        data = {
            "id": supplier.id,
            "ruc": supplier.ruc,
            "company_name": supplier.company_name,
            "business_name": supplier.business_name,
            "representative": supplier.representative,
            "phone": supplier.phone,
            "email": supplier.email,
            "address": supplier.address,
            "account_number": supplier.account_number,
            "region": (
                {"id": supplier.region.id, "name": supplier.region.name}
                if supplier.region else None
            ),
            "province": (
                {"id": supplier.province.id, "name": supplier.province.name}
                if supplier.province else None
            ),
            "district": (
                {"id": supplier.district.id, "name": supplier.district.name}
                if supplier.district else None
            ),
            "created_at": supplier.created_at.isoformat() if supplier.created_at else None,
            "updated_at": supplier.updated_at.isoformat() if supplier.updated_at else None
        }
        return JsonResponse(data)
    except Supplier.DoesNotExist:
        return JsonResponse({"error": "Proveedor no encontrado"}, status=404)
