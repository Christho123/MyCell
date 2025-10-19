import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models.employee import Employees
from datetime import datetime


@csrf_exempt
def employee_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = Employees.objects.select_related("document_type", "rol", "region", "province", "district")
    data = []
    for e in qs:
        data.append({
            "id": e.id,
            "name": e.name,
            "last_name_paternal": e.last_name_paternal,
            "last_name_maternal": e.last_name_maternal,
            "full_name": e.get_full_name(),
            "document_type": (
                {"id": e.document_type.id, "name": e.document_type.name}
                if e.document_type else None
            ),
            "document_number": e.document_number,
            "email": e.email,
            "gender": e.gender,
            "phone": e.phone,
            "birth_date": e.birth_date.isoformat() if e.birth_date else None,
            "region": (
                {"id": e.region.id, "name": e.region.name}
                if e.region else None
            ),
            "province": (
                {"id": e.province.id, "name": e.province.name}
                if e.province else None
            ),
            "district": (
                {"id": e.district.id, "name": e.district.name}
                if e.district else None
            ),
            "rol": (
                {"id": e.rol.id, "name": e.rol.name}
                if e.rol else None
            ),
            "salary": e.salary,
            "address": e.address,
            "created_at": e.created_at.isoformat() if e.created_at else None,
            "updated_at": e.updated_at.isoformat() if e.updated_at else None
        })
    return JsonResponse({"employees": data})


@csrf_exempt
def employee_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)

    try:
        birth_date_str = payload.get("birth_date")

        if not birth_date_str:
            birth_date = None
        else:
            try:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Formato de fecha inválido. Usa AAAA-MM-DD."}, status=400)

        employee_data = {
            'name': payload.get('name'),
            'last_name_paternal': payload.get('last_name_paternal'),
            'last_name_maternal': payload.get('last_name_maternal'),
            'document_type_id': payload.get('document_type'),
            'document_number': payload.get('document_number'),
            'email': payload.get('email'),
            'gender': payload.get('gender'),
            'phone': payload.get('phone'),
            'birth_date': birth_date,
            'region_id': payload.get('region'),
            'province_id': payload.get('province'),
            'district_id': payload.get('district'),
            'rol_id': payload.get('rol'),
            'salary': payload.get('salary'),
            'address': payload.get('address'),
        }

        filtered_data = {k: v for k, v in employee_data.items() if v is not None}
        e = Employees.objects.create(**filtered_data)
        
        response_data = {
            "message": "Empleado creado exitosamente",
            "employee": {
                "id": e.id,
                "name": e.name,
                "last_name_paternal": e.last_name_paternal,
                "last_name_maternal": e.last_name_maternal,
                "full_name": e.get_full_name(),
                "document_type": (
                    {"id": e.document_type.id, "name": e.document_type.name}
                    if e.document_type else None
                ),
                "document_number": e.document_number,
                "email": e.email,
                "gender": e.gender,
                "phone": e.phone,
                "birth_date": e.birth_date.isoformat() if e.birth_date else None,
                "region": (
                    {"id": e.region.id, "name": e.region.name}
                    if e.region else None
                ),
                "province": (
                    {"id": e.province.id, "name": e.province.name}
                    if e.province else None
                ),
                "district": (
                    {"id": e.district.id, "name": e.district.name}
                    if e.district else None
                ),
                "rol": (
                    {"id": e.rol.id, "name": e.rol.name}
                    if e.rol else None
                ),
                "salary": e.salary,
                "address": e.address,
                "created_at": e.created_at.isoformat() if e.created_at else None,
                "updated_at": e.updated_at.isoformat() if e.updated_at else None
            }
        }
        
        return JsonResponse(response_data, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error al crear al empleado: {str(e)}"}, status=500)


@csrf_exempt
def employee_update(request, pk):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponseNotAllowed(["PUT", "PATCH"])
    
    # Buscar empleado
    try:
        employee = Employees.objects.get(pk=pk)
    except Employees.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
    
    # Leer JSON
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)
    
    # Campos permitidos
    allowed_fields = {
        'name': 'name',
        'last_name_paternal': 'last_name_paternal',
        'last_name_maternal': 'last_name_maternal',
        'document_type': 'document_type_id',
        'document_number': 'document_number',
        'email': 'email',
        'gender': 'gender',
        'phone': 'phone',
        'birth_date': 'birth_date',
        'region': 'region_id',
        'province': 'province_id',
        'district': 'district_id',
        'rol': 'rol_id',
        'salary': 'salary',
        'address': 'address',
    }

    # Aplicar cambios solo a los campos presentes
    for field_name, model_field in allowed_fields.items():
        if field_name in payload:
            value = payload[field_name]

            # Si el campo es fecha, convertirla correctamente
            if field_name == "birth_date" and value:
                from datetime import date
                try:
                    value = date.fromisoformat(value)
                except ValueError:
                    return JsonResponse({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

            setattr(employee, model_field, value)
    
    # Guardar cambios sin exigir campos obligatorios en payload
    employee.save(update_fields=list(allowed_fields.values()))
    
    # Respuesta con datos actualizados
    updated_data = {
        "id": employee.id,
        "name": employee.name,
        "last_name_paternal": employee.last_name_paternal,
        "last_name_maternal": employee.last_name_maternal,
        "document_type": (
            {"id": employee.document_type.id, "name": employee.document_type.name}
            if employee.document_type else None
        ),
        "document_number": employee.document_number,
        "email": employee.email,
        "gender": employee.gender,
        "phone": employee.phone,
        "birth_date": employee.birth_date.isoformat() if employee.birth_date else None,
        "region": (
            {"id": employee.region.id, "name": employee.region.name}
            if employee.region else None
        ),
        "province": (
            {"id": employee.province.id, "name": employee.province.name}
            if employee.province else None
        ),
        "district": (
            {"id": employee.district.id, "name": employee.district.name}
            if employee.district else None
        ),
        "rol": (
            {"id": employee.rol.id, "name": employee.rol.name}
            if employee.rol else None
        ),
        "salary": employee.salary,
        "address": employee.address,
        "updated_at": employee.updated_at.isoformat() if employee.updated_at else None
    }
    
    return JsonResponse({
        "message": "Empleado actualizado parcialmente con éxito",
        "employee": updated_data
    }, status=200)



@csrf_exempt
def employee_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    
    try:
        e = Employees.objects.get(pk=pk)
    except Employees.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    e.delete()
    return JsonResponse({"message": "Empleado eliminado exitosamente",
                         "status": "deleted",
                         "employee_id": pk})


@csrf_exempt
def employee_detail(request, pk):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    try:
        employee = Employees.objects.select_related("document_type", "rol", "region", "province", "district").get(pk=pk)
        data = {
            "id": employee.id,
            "name": employee.name,
            "last_name_paternal": employee.last_name_paternal,
            "last_name_maternal": employee.last_name_maternal,
            "full_name": employee.get_full_name(),
            "document_type": (
                {"id": employee.document_type.id, "name": employee.document_type.name}
                if employee.document_type else None
            ),
            "document_number": employee.document_number,
            "email": employee.email,
            "gender": employee.gender,
            "phone": employee.phone,
            "birth_date": employee.birth_date.isoformat() if employee.birth_date else None,
            "region": (
                {"id": employee.region.id, "name": employee.region.name}
                if employee.region else None
            ),
            "province": (
                {"id": employee.province.id, "name": employee.province.name}
                if employee.province else None
            ),
            "district": (
                {"id": employee.district.id, "name": employee.district.name}
                if employee.district else None
            ),
            "rol": (
                {"id": employee.rol.id, "name": employee.rol.name}
                if employee.rol else None
            ),
            "salary": employee.salary,
            "address": employee.address,
            "created_at": employee.created_at.isoformat() if employee.created_at else None,
            "updated_at": employee.updated_at.isoformat() if employee.updated_at else None
        }
        return JsonResponse(data)
    except Employees.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
