from typing import Iterable, Optional
from django.utils import timezone
from ..models.payment_type import PaymentType

def list_active() -> Iterable[PaymentType]:
    return PaymentType.objects.filter(deleted_at__isnull=True).order_by("name")

def get_by_id(pk: int) -> Optional[PaymentType]:
    try:
        return PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
    except PaymentType.DoesNotExist:
        return None

def create(**kwargs) -> PaymentType:
    return PaymentType.objects.create(**kwargs)

def update(instance: PaymentType, **kwargs) -> PaymentType:
    for field_name, value in kwargs.items():
        setattr(instance, field_name, value)
    instance.save()
    return instance

def soft_delete(instance: PaymentType) -> PaymentType:
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["deleted_at"]) 
    return instance




