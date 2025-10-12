from typing import Iterable, Optional
from django.utils import timezone
from ..models.document_type import DocumentType

def list_active() -> Iterable[DocumentType]:
    return DocumentType.objects.filter(deleted_at__isnull=True).order_by("name")

def get_by_id(pk: int) -> Optional[DocumentType]:
    try:
        return DocumentType.objects.get(pk=pk, deleted_at__isnull=True)
    except DocumentType.DoesNotExist:
        return None

def create(**kwargs) -> DocumentType:
    return DocumentType.objects.create(**kwargs)

def update(instance: DocumentType, **kwargs) -> DocumentType:
    for field_name, value in kwargs.items():
        setattr(instance, field_name, value)
    instance.save()
    return instance

def soft_delete(instance: DocumentType) -> DocumentType:
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["deleted_at"]) 
    return instance




