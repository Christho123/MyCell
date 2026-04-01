from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path
import csv

from products_configurations.models import Brand
from ubi_geo.models import Country

# IDs numéricos del CSV db/brands.csv (otra BD / snapshot); se mapean a ISO2 de `countries`.
# Tras `import_ubigeo` o cargar countries.csv, el PK ya no coincide con estos números.
LEGACY_COUNTRY_ID_TO_ISO2 = {
    "42": "CN",
    "66": "US",
    "125": "JP",
    "222": "TW",
    "167": "NG",
    "216": "CH",
    "50": "KR",
    "92": "CN",
}


def getv(row, *cands):
    """Devuelve el primer valor no vacío encontrado en las columnas dadas."""
    for k in cands:
        if k in row:
            v = (row.get(k) or "").strip()
            if v != "":
                return v
    return ""


class Command(BaseCommand):
    help = (
        "Importa marcas (Brand) desde un CSV con ';'. "
        "País: columna opcional country_iso2 (ISO2), o country_id (PK o legacy del CSV brands)."
    )

    def resolve_country(self, row):
        """Resuelve Country por country_iso2, por PK, o por mapa legacy ID→ISO2."""
        iso = getv(row, "country_iso2", "country_iso", "ISO2_country")
        if iso:
            c = Country.objects.filter(ISO2__iexact=iso.strip()).first()
            if c:
                return c
            self.stdout.write(self.style.WARNING(f"País ISO2={iso!r} no encontrado (¿countries en BD?)"))
            return None

        raw = getv(row, "country_id", "Country_id", "country")
        if not raw:
            return None

        raw = raw.strip()
        if raw.isdigit():
            c = Country.objects.filter(pk=int(raw)).first()
            if c:
                return c
            iso2 = LEGACY_COUNTRY_ID_TO_ISO2.get(raw)
            if iso2:
                c = Country.objects.filter(ISO2__iexact=iso2).first()
                if c:
                    return c
            self.stdout.write(
                self.style.WARNING(
                    f"País country_id={raw} sin coincidencia ni legacy ISO2; "
                    f"importa countries o usa columna country_iso2."
                )
            )
            return None

        return Country.objects.filter(ISO2__iexact=raw.upper()).first()

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="db/brands.csv",
            help="Ruta del archivo CSV con las marcas (por defecto: db/brands.csv)",
        )
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Borra todas las marcas antes de importar.",
        )

    def handle(self, *args, **opt):
        csv_path = Path(opt["path"]).resolve()

        if not csv_path.exists():
            raise CommandError(f"No se encontró el archivo: {csv_path}")

        if opt["truncate"]:
            self.stdout.write(self.style.WARNING("Eliminando todas las marcas existentes..."))
            Brand.objects.all().delete()

        self.stdout.write(f"Importando marcas desde {csv_path}…")

        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            created = updated = skipped = 0

            with transaction.atomic():
                for row in reader:
                    name = getv(row, "name", "Name")
                    description = getv(row, "description", "Description")

                    if not name:
                        skipped += 1
                        continue

                    country = self.resolve_country(row)
                    if not country:
                        self.stdout.write(self.style.WARNING(f"Sin país válido para marca {name!r}, omitiendo"))
                        skipped += 1
                        continue

                    obj, created_flag = Brand.objects.update_or_create(
                        name=name,
                        defaults={
                            "description": description,
                            "country": country,
                        },
                    )

                    if created_flag:
                        created += 1
                    else:
                        updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importación completada ✔  Nuevas: {created} | Actualizadas: {updated} | Omitidas: {skipped}"
        ))
