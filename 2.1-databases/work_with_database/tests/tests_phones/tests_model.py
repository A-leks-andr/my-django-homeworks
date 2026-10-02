from decimal import Decimal

import pytest
from django.db import IntegrityError, models
from django.utils.text import slugify
from phones.models import Phone


def test_phone_str_returns_name(phone_factory):
    phone = phone_factory(name="Iphone X")

    assert str(phone) == "Iphone X"


def test_phone_save_generates_slug_from_name(phone_factory):
    """Если slug не задан, при сохранении он формируется из name через slugify."""
    phone = phone_factory(name="Nokia 8")

    assert phone.slug == slugify("Nokia 8")
    assert phone.slug == "nokia-8"


def test_phone_save_keeps_manual_slug(phone_factory):
    """Явно переданный slug не должен перезаписываться при сохранении."""
    phone = phone_factory(name="Iphone X", slug="iphone-x-2024")

    assert phone.slug == "iphone-x-2024"


def test_phone_slug_stable_after_resave(phone_factory):
    """Повторное сохранение не меняет уже сгенерированный slug."""
    phone = phone_factory(name="Samsung Galaxy Edge 2")

    phone.price = Decimal("75000.00")
    phone.save()
    phone.refresh_from_db()

    assert phone.slug == "samsung-galaxy-edge-2"


def test_phone_slug_is_unique(phone_factory):
    """Поле slug уникально: второй телефон с тем же name создать нельзя."""
    phone_factory(name="Iphone X")

    with pytest.raises(IntegrityError):
        phone_factory(name="Iphone X")


def test_phone_created_with_all_fields(phone_factory):
    phone = phone_factory(
        name="Nokia 8",
        image="https://example.com/nokia-8.jpg",
        price="19999.99",
        release_date="2013-01-20",
        lte_exists=False,
    )
    phone.refresh_from_db()

    assert phone.id is not None
    assert phone.name == "Nokia 8"
    assert phone.image == "https://example.com/nokia-8.jpg"
    assert phone.price == Decimal("19999.99")
    assert str(phone.release_date) == "2013-01-20"
    assert phone.lte_exists is False


def test_phone_model_fields():
    id_field = Phone._meta.get_field("id")
    assert isinstance(id_field, models.AutoField)
    assert id_field.primary_key is True

    name_field = Phone._meta.get_field("name")
    assert isinstance(name_field, models.CharField)
    assert name_field.max_length == 100

    image_field = Phone._meta.get_field("image")
    assert isinstance(image_field, models.URLField)

    price_field = Phone._meta.get_field("price")
    assert isinstance(price_field, models.DecimalField)
    assert price_field.max_digits == 10
    assert price_field.decimal_places == 2

    release_date_field = Phone._meta.get_field("release_date")
    assert isinstance(release_date_field, models.DateField)

    lte_exists_field = Phone._meta.get_field("lte_exists")
    assert isinstance(lte_exists_field, models.BooleanField)

    slug_field = Phone._meta.get_field("slug")
    assert isinstance(slug_field, models.SlugField)
    assert slug_field.max_length == 110
    assert slug_field.unique is True
    assert slug_field.blank is True
