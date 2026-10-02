import pytest
from model_bakery import baker
from phones.models import Phone


@pytest.fixture(autouse=True)
def enable_db_for_all_tests(db):
    pass


@pytest.fixture
def phone_factory():
    def factory(*args, **kwargs):
        return baker.make(Phone, *args, **kwargs)

    return factory
