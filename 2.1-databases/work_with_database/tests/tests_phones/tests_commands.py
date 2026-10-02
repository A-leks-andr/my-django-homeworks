import csv
from datetime import datetime
from decimal import Decimal

from django.core.management import call_command
from django.utils.text import slugify
from phones.models import Phone


def _csv_rows():
    """Читает phones.csv так же, как команда import_phones."""
    with open("phones.csv", "r") as file:
        return list(csv.DictReader(file, delimiter=";"))


def test_import_phones_creates_records_for_every_row():
    """Команда создаёт по записи на каждую строку CSV."""
    rows = _csv_rows()

    call_command("import_phones")

    assert Phone.objects.count() == len(rows)


def test_import_phones_parses_all_fields():
    """Поля импортируются корректно: price — Decimal,
    lte_exists — bool, slug генерируется."""
    call_command("import_phones")

    first_row = _csv_rows()[0]
    phone = Phone.objects.get(id=first_row["id"])
    expected_date = datetime.strptime(first_row["release_date"], "%Y-%m-%d").date()

    assert phone.name == first_row["name"]
    assert phone.image == first_row["image"]
    assert phone.price == Decimal(first_row["price"])
    assert phone.release_date == expected_date
    assert phone.lte_exists is (first_row["lte_exists"].lower() == "true")
    assert phone.slug == slugify(first_row["name"])


def test_import_phones_is_idempotent():
    """Повторный запуск не создаёт дубликатов (update_or_create по id)."""
    rows = _csv_rows()

    call_command("import_phones")
    call_command("import_phones")

    assert Phone.objects.count() == len(rows)
