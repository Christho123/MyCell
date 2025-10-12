from typing import Iterable, Optional
from django.utils import timezone
from ..models.payment_status import PaymentStatus

def list_active() -> Iterable[PaymentStatus]:
    return PaymentStatus.objects.filter(deleted_at__isnull=True).order_by("name")

def get_by_id(pk: int) -> Optional[PaymentStatus]:
    try:
        return PaymentStatus.objects.get(pk=pk, deleted_at__isnull=True)
    except PaymentStatus.DoesNotExist:
        return None

def create(**kwargs) -> PaymentStatus:
    return PaymentStatus.objects.create(**kwargs)

def update(instance: PaymentStatus, **kwargs) -> PaymentStatus:
    for field_name, value in kwargs.items():
        setattr(instance, field_name, value)
    instance.save()
    return instance

def soft_delete(instance: PaymentStatus) -> PaymentStatus:
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["deleted_at"]) 
    return instance




